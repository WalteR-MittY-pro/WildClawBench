from __future__ import annotations

import json
import logging
import os
import shlex
import subprocess
import time
from pathlib import Path

from dotenv import load_dotenv

from src.agents.base import AgentExecution, AgentTaskSpec, BaseAgent
from src.utils.grading import extract_usage_from_jsonl
from src.utils.docker_utils import (
    inject_lobster_workspace,
    inject_openclaw_models,
    run_background,
    run_warmup,
    setup_skills,
    setup_workspace,
    start_container,
)

load_dotenv()

logger = logging.getLogger(__name__)


class OpenClawAgent(BaseAgent):
    def __init__(
        self,
        gateway_port: int,
        openrouter_api_key: str = "",
        openrouter_base_url: str = "https://openrouter.ai/api/v1",
        image_model: str | None = None,
    ) -> None:
        self.gateway_port = gateway_port
        self.openrouter_api_key = openrouter_api_key
        self.openrouter_base_url = openrouter_base_url
        self.image_model = image_model if image_model is not None else os.environ.get("OPENCLAW_IMAGE_MODEL", "").strip()

    @property
    def expects_gateway(self) -> bool:
        return True

    @property
    def transcript_container_path(self) -> str:
        return "/root/.openclaw/agents/main/sessions/chat.jsonl"

    def run_task(self, spec: AgentTaskSpec) -> AgentExecution:
        gateway_proc = None
        agent_proc = None
        elapsed_time = float(spec.timeout_seconds)

        try:
            exec_path = os.path.join(spec.workspace_path, "exec")
            tmp_path = os.path.join(spec.workspace_path, "tmp")
            os.makedirs(exec_path, exist_ok=True)

            start_container(
                spec.task_id,
                exec_path,
                extra_env=spec.task.get("env", ""),
                tmp_path=tmp_path,
                lobster_env=spec.lobster.get("env") if spec.lobster else None,
                direct_env=spec.direct_env,
            )
            if spec.lobster:
                inject_lobster_workspace(spec.task_id, spec.lobster["workspace"])

            setup_workspace(spec.task_id, thinking=spec.thinking)
            setup_skills(spec.task_id, spec.task.get("skills", ""), spec.task.get("skills_path", ""))
            run_warmup(spec.task_id, spec.task.get("warmup", ""))

            if spec.models_config:
                inject_openclaw_models(spec.task_id, spec.models_config)
                # Use model from models_config if available
                module_models = spec.models_config.get("moduleModels", {})
                agent_model = module_models.get("openclaw_agent") or spec.model
                self._set_model(spec.task_id, agent_model)
                self._inject_provider_auth(spec.task_id, spec.models_config)
            else:
                self._set_model(spec.task_id, spec.model)
                self._inject_provider_auth(spec.task_id)
            image_model = self.image_model or spec.model
            self._set_image_model(spec.task_id, image_model)

            gateway_env = {
                "OPENROUTER_API_KEY": self.openrouter_api_key,
                "OPENROUTER_BASE_URL": self.openrouter_base_url,
            }
            gateway_env.update(spec.direct_env or {})
            env_prefix = " ".join(
                f"export {key}={shlex.quote(value)} &&"
                for key, value in gateway_env.items()
                if value
            )
            gateway_proc = run_background(
                spec.task_id,
                bash_cmd=f"{env_prefix} openclaw gateway --port {self.gateway_port}",
                log_path=spec.output_dir / "gateway.log",
            )
            logger.info("[%s] Waiting for gateway to be ready (2s)...", spec.task_id)
            time.sleep(2)

            safe_prompt = spec.prompt.replace("'", "'\\''")
            start_time = time.perf_counter()
            agent_proc = run_background(
                spec.task_id,
                bash_cmd=f"openclaw agent --session-id chat --timeout {spec.timeout_seconds} --message '{safe_prompt}'",
                log_path=spec.output_dir / "agent.log",
            )

            logger.info("[%s] Waiting for agent to finish...", spec.task_id)
            try:
                agent_proc.wait(timeout=spec.timeout_seconds)
                elapsed_time = time.perf_counter() - start_time
                logger.info(
                    "[%s] Agent finished successfully, elapsed: %.2f seconds",
                    spec.task_id,
                    elapsed_time,
                )
            except subprocess.TimeoutExpired:
                logger.info("[%s] Agent timed out...", spec.task_id)
                elapsed_time = float(spec.timeout_seconds)
                agent_proc.kill()
                agent_proc.wait()

            logger.info("[%s] Agent exit code: %s", spec.task_id, agent_proc.returncode)
            return AgentExecution(
                elapsed_time=elapsed_time,
                error=None,
                gateway_proc=gateway_proc,
                agent_proc=agent_proc,
            )
        except Exception as exc:
            logger.error("[%s] Execution error: %s", spec.task_id, exc)
            return AgentExecution(
                elapsed_time=float(spec.timeout_seconds),
                error=str(exc),
                gateway_proc=gateway_proc,
                agent_proc=agent_proc,
            )

    def collect_usage(self, task_id: str, output_dir: Path, elapsed_time: float) -> dict:
        transcript_host = output_dir / "chat.jsonl"
        output_dir.mkdir(parents=True, exist_ok=True)
        r_cp = subprocess.run(
            ["docker", "cp", f"{task_id}:{self.transcript_container_path}", str(transcript_host)],
            capture_output=True,
            text=True,
        )
        if r_cp.returncode == 0 and transcript_host.exists():
            usage = extract_usage_from_jsonl(transcript_host)
        else:
            logger.warning("[%s] Transcript copy failed: %s", task_id, r_cp.stderr.strip())
            usage = {
                "input_tokens": 0,
                "output_tokens": 0,
                "cache_read_tokens": 0,
                "cache_write_tokens": 0,
                "total_tokens": 0,
                "cost_usd": 0.0,
                "request_count": 0,
            }
        usage["elapsed_time"] = round(elapsed_time, 2)
        return usage

    def _set_model(self, task_id: str, model: str) -> None:
        r = subprocess.run(
            ["docker", "exec", task_id, "/bin/bash", "-c", f"openclaw models set '{model}'"],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            raise RuntimeError(f"Model setup failed:\n{r.stderr}")
        logger.info("[%s] Model set: %s", task_id, model)

    def _inject_provider_auth(
        self,
        task_id: str,
        models_config: dict | None = None,
    ) -> None:
        providers = (models_config or {}).get("providers", {})
        profiles: dict[str, dict[str, str]] = {}
        if isinstance(providers, dict) and providers:
            for provider_name, provider_cfg in providers.items():
                provider_name = str(provider_name)
                if not isinstance(provider_cfg, dict):
                    continue
                api_key = str(provider_cfg.get("apiKey") or "").strip()
                if not api_key:
                    continue
                profiles[f"{provider_name}:default"] = {
                    "type": "api_key",
                    "provider": provider_name,
                    "key": api_key,
                }
        elif self.openrouter_api_key:
            profiles["openrouter:default"] = {
                "type": "api_key",
                "provider": "openrouter",
                "key": self.openrouter_api_key,
            }

        if not profiles:
            return

        auth_profile_path = "/root/.openclaw/agents/main/agent/auth-profiles.json"
        profiles_json = json.dumps(profiles)
        inject_cmd = f"""python3 - <<'PY'
import json
import pathlib

p = pathlib.Path("{auth_profile_path}")
d = json.loads(p.read_text()) if p.exists() else {{"version": 1, "profiles": {{}}}}
d.setdefault("version", 1)
d.setdefault("profiles", {{}}).update({profiles_json})
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(d, indent=2))
PY"""
        r = subprocess.run(
            ["docker", "exec", task_id, "/bin/bash", "-c", inject_cmd],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            logger.warning(
                "[%s] Auth profile injection failed: %s",
                task_id,
                r.stderr.strip(),
            )
            return
        logger.info(
            "[%s] Injected provider auth profiles: %s",
            task_id,
            ", ".join(profiles.keys()),
        )

    def _set_image_model(self, task_id: str, model: str) -> None:
        subprocess.run(
            ["docker", "exec", task_id, "/bin/bash", "-c", f"openclaw config set agents.defaults.imageModel.primary '{model}'"],
            capture_output=True,
            text=True,
        )
        logger.info("[%s] imageModel set: %s", task_id, model)

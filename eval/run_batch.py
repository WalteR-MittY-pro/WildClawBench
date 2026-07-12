from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
import sys
import time
import json
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.base import AgentTaskSpec, BaseAgent
from src.agents.claudecode import ClaudeCodeAgent
from src.agents.codex import CodexAgent
from src.agents.openclaw import OpenClawAgent
from src.utils.cli_args import parse_run_batch_args
from src.utils.endpoint_utils import (
    normalize_openrouter_base_url_for_claudecode,
    normalize_openrouter_base_url_for_openclaw,
)
from src.utils.task_parser import parse_task_md
from src.utils.docker_utils import (
    remove_container,
    close_proc_log,
    collect_output_from_container,
    TMP_WORKSPACE,
)
from src.utils.grading import (
    run_grading,
    format_scores,
    print_summary,
    print_global_summary,
    write_error_score as write_error_score_file,
)

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

GATEWAY_PORT     = int(os.environ.get("GATEWAY_PORT", "18789"))

ROOT_DIR         = Path(__file__).resolve().parent.parent
TASKS_DIR        = ROOT_DIR / os.environ.get("TASKS_SUBDIR",  "tasks")
OUTPUT_DIR       = ROOT_DIR / os.environ.get("OUTPUT_SUBDIR", "output")

DEFAULT_MODEL    = os.environ.get("DEFAULT_MODEL",    "openrouter/anthropic/claude-sonnet-4.6")
DEFAULT_PARALLEL = int(os.environ.get("DEFAULT_PARALLEL", "1"))
DEFAULT_RATE_LIMIT_RETRIES = int(os.environ.get("RATE_LIMIT_RETRIES", "0"))
DEFAULT_RATE_LIMIT_WAIT_SECONDS = float(os.environ.get("RATE_LIMIT_WAIT_SECONDS", "120"))

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL_OPENCLAW = normalize_openrouter_base_url_for_openclaw(
    os.environ.get("OPENROUTER_BASE_URL", "")
)
OPENROUTER_BASE_URL_CLAUDECODE = normalize_openrouter_base_url_for_claudecode(
    os.environ.get("OPENROUTER_BASE_URL", "")
)
MODELS_ENV_PLACEHOLDER_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
AGENT_SKILLS_PROMPT_DIR = "~/.openclaw/skills"
RATE_LIMIT_RETRY_ELAPSED_TIME = 1200.0
RATE_LIMIT_RETRY_OVERALL_SCORE = 0.0

ALL_CATEGORIES = [
    "01_Productivity_Flow",
    "02_Code_Intelligence",
    "03_Social_Interaction",
    "04_Search_Retrieval",
    "05_Creative_Synthesis",
    "06_Safety_Alignment",
]


def resolve_output_root(output_dir: Path, agent_backend: str) -> Path:
    return output_dir if agent_backend == "openclaw" else output_dir / agent_backend


def detect_rate_limit_signal(output_dir: Path) -> str | None:
    usage_path = output_dir / "usage.json"
    score_path = output_dir / "score.json"
    usage = _read_json_object(usage_path)
    score = _read_json_object(score_path)
    if usage is None or score is None:
        return None

    elapsed_time = _json_float(usage.get("elapsed_time"))
    overall_score = _json_float(score.get("overall_score"))
    if (
        elapsed_time == RATE_LIMIT_RETRY_ELAPSED_TIME
        and overall_score == RATE_LIMIT_RETRY_OVERALL_SCORE
    ):
        return f"{usage_path} + {score_path}"
    return None


def _read_json_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _json_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def existing_task_runs(output_root: Path, task: dict) -> list[Path]:
    task_dir = output_root / str(task["category"]) / str(task["task_id"])
    if not task_dir.is_dir():
        return []
    return sorted(path for path in task_dir.iterdir() if path.is_dir())


def partition_tasks_by_existing_runs(
    tasks: list[dict],
    output_root: Path,
) -> tuple[list[dict], list[tuple[dict, list[Path]]]]:
    pending_tasks: list[dict] = []
    skipped_tasks: list[tuple[dict, list[Path]]] = []

    for task in tasks:
        runs = existing_task_runs(output_root, task)
        if runs:
            skipped_tasks.append((task, runs))
        else:
            pending_tasks.append(task)

    return pending_tasks, skipped_tasks

def grade_the_task(
    task_id: str,
    workspace_path: str,
    output_dir: Path,
    task: dict,
    result: dict,
    lobster_env: list[str] | None = None,
    transcript_container_path: str = "",
    grade_on_error: bool = False,
    write_error_score_on_failure: bool = False,
):
    gt_host = os.path.join(workspace_path, "gt")
    if os.path.isdir(gt_host):
        r_gt = subprocess.run(
            ["docker", "cp", gt_host, f"{task_id}:{TMP_WORKSPACE}/gt"],
            capture_output=True, text=True,
        )
        if r_gt.returncode != 0:
            logger.warning("[%s] gt directory copy failed: %s", task_id, r_gt.stderr)
        else:
            logger.info("[%s] gt directory copied to container %s/gt", task_id, TMP_WORKSPACE)

    should_grade = task.get("automated_checks") and (
        not result.get("error") or grade_on_error
    )
    if should_grade:
        try:
            scores = run_grading(
                task_id=task_id,
                automated_checks=task["automated_checks"],
                output_dir=output_dir,
                extra_env=task.get("env", ""),
                lobster_env=lobster_env,
                transcript_container_path=transcript_container_path,
                write_error_score=write_error_score_on_failure,
            )
            result["scores"] = scores
            print(format_scores(task_id, scores))
            logger.info("[%s] Grading complete", task_id)
        except Exception as exc:
            logger.error("[%s] Grading failed: %s", task_id, exc)
            result["scores"] = write_error_score_file(output_dir, task_id, str(exc))
    elif not task.get("automated_checks"):
        logger.info("[%s] No Automated Checks, skipping grading", task_id)
        if result.get("error"):
            result["scores"] = write_error_score_file(output_dir, task_id, result["error"])

    return result

def save_usage(output_dir: Path, result: dict, usage: dict, task_id: str) -> dict:
    result["usage"] = usage
    if usage["request_count"] > 0:
        logger.info(
            "[%s] Token usage - input:%d output:%d cache_read:%d total:%d cost:$%.4f",
            task_id,
            usage["input_tokens"], usage["output_tokens"],
            usage["cache_read_tokens"], usage["total_tokens"],
            usage["cost_usd"],
        )
    usage_path = output_dir / "usage.json"
    usage_path.write_text(
        json.dumps(usage, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    logger.info("[%s] Usage written to %s", task_id, usage_path)
    return result

def collect_task_output(
    task_id: str,
    output_dir: Path,
    *,
    include_workspace_changes: bool = False,
) -> None:
    """Collect task output files from the container to output_dir/task_output/."""
    try:
        collect_output_from_container(
            task_id,
            output_dir,
            include_workspace_changes=include_workspace_changes,
        )
    except Exception as exc:
        logger.warning("[%s] Failed to collect task output: %s", task_id, exc)


def load_models_config(models_config_path: Path) -> dict:
    raw_config = models_config_path.read_text(encoding="utf-8")
    expanded_config = expand_models_config_env(raw_config)
    parsed_models_config = json.loads(expanded_config)
    return _normalize_models_config(parsed_models_config, models_config_path)


def _normalize_models_config(models_config: dict, source: Path) -> dict:
    if not isinstance(models_config, dict):
        raise ValueError(f"Models config must be a JSON object: {source}")
    if "providers" not in models_config and isinstance(models_config.get("models"), dict):
        models_config = models_config["models"]

    providers = models_config.get("providers")
    if not isinstance(providers, dict):
        raise ValueError(f"Models config must contain a top-level providers object: {source}")

    normalized = dict(models_config)
    normalized.setdefault("mode", "merge")
    normalized_providers = {}
    for provider_name, provider_config in providers.items():
        if not isinstance(provider_config, dict):
            raise ValueError(f"Provider config for {provider_name!r} must be a JSON object: {source}")
        provider = dict(provider_config)
        models = provider.get("models", [])
        if isinstance(models, dict):
            provider["models"] = [
                {"id": model_id, "name": model_id, **(entry if isinstance(entry, dict) else {})}
                for model_id, entry in models.items()
            ]
        elif not isinstance(models, list) or not all(isinstance(entry, dict) for entry in models):
            raise ValueError(f"Provider models for {provider_name!r} must be a JSON object or array: {source}")
        normalized_providers[str(provider_name)] = provider
    normalized["providers"] = normalized_providers
    return normalized


def resolve_judge_env(models_config: dict | None, requested_model: str) -> dict[str, str]:
    if not models_config:
        return {}

    module_models = models_config.get("moduleModels", {})
    judge_model = (
        str(module_models.get("judge") or requested_model)
        if isinstance(module_models, dict)
        else requested_model
    )
    provider_name, provider, model_entry = _select_model_provider(models_config, judge_model)
    base_url = str(provider.get("baseUrl") or provider.get("base_url") or "").rstrip("/")
    api_key = str(provider.get("apiKey") or provider.get("api_key") or "")
    model = str((model_entry or {}).get("id") or provider.get("model") or "")
    display = str((model_entry or {}).get("name") or (f"{provider_name}/{model}" if model else judge_model))
    if not base_url or not api_key or not model:
        return {}
    return {
        "COEVO_JUDGE_API_KEY": api_key,
        "COEVO_JUDGE_BASE_URL": base_url,
        "COEVO_JUDGE_MODEL": model,
        "COEVO_JUDGE_DISPLAY_MODEL": display,
        "OPENROUTER_API_KEY": api_key,
        "OPENROUTER_BASE_URL": base_url,
        "JUDGE_MODEL": model,
    }


def _select_model_provider(
    models_config: dict[str, Any],
    requested_model: str,
) -> tuple[str, dict[str, Any], dict[str, Any] | None]:
    providers = models_config.get("providers", {})
    if not isinstance(providers, dict):
        return "default", models_config, None
    for provider_name, provider in providers.items():
        if not isinstance(provider, dict):
            continue
        for model_entry in _model_entries(provider):
            model_id = str(model_entry.get("id") or "")
            aliases = {model_id, str(model_entry.get("name") or ""), f"{provider_name}/{model_id}"}
            if requested_model in aliases:
                return str(provider_name), provider, model_entry
    for provider_name, provider in providers.items():
        if isinstance(provider, dict):
            entries = _model_entries(provider)
            return str(provider_name), provider, entries[0] if entries else None
    return "default", models_config, None


def _model_entries(provider: dict[str, Any]) -> list[dict[str, Any]]:
    models = provider.get("models")
    if not isinstance(models, list):
        return []
    return [entry for entry in models if isinstance(entry, dict)]


def expand_models_config_env(raw_config: str) -> str:
    def replacement(match: re.Match[str]) -> str:
        env_name = match.group(1)
        value = os.environ.get(env_name)
        if not value:
            raise ValueError(
                f"{env_name} must be set to a non-empty value when models config uses ${{{env_name}}}"
            )
        return value

    return MODELS_ENV_PLACEHOLDER_RE.sub(replacement, raw_config)


def build_skill_read_prompt(skills: str) -> str:
    skill_names = [line.strip() for line in skills.splitlines() if line.strip()]
    if not skill_names:
        return ""
    skill_paths = "\n".join(f"- {AGENT_SKILLS_PROMPT_DIR}/{Path(name).name}/SKILL.md" for name in skill_names)
    return (
        "Task-specific skills are installed in the container.\n"
        "Before solving the task, read the relevant SKILL.md file(s) below and follow them:\n"
        f"{skill_paths}\n\n"
    )


def merge_skill_dir_override(skills: str, skills_path: str, skill_dir: str) -> tuple[str, str]:
    skill_dir_path = Path(skill_dir).expanduser().resolve()
    if not skill_dir_path.is_dir() or not (skill_dir_path / "SKILL.md").is_file():
        raise ValueError(f"skill_dir must point to a runtime skill containing SKILL.md: {skill_dir}")
    original_skills = _skill_names(skills)
    merged_skills = [name for name in original_skills if Path(name).name != skill_dir_path.name]
    merged_skills.append(skill_dir_path.name)
    overlay_root = skill_dir_path.parent / f"{skill_dir_path.name}__merged_skills"
    shutil.rmtree(overlay_root, ignore_errors=True)
    overlay_root.mkdir(parents=True, exist_ok=True)
    source_root = Path(skills_path).expanduser()
    for name in original_skills:
        source = source_root / name
        if Path(name).name == skill_dir_path.name:
            continue
        destination = overlay_root / name
        if source.is_dir():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, destination)
            continue
        markdown_source = source_root / f"{name}.md"
        if markdown_source.is_file():
            destination.mkdir(parents=True, exist_ok=True)
            shutil.copy2(markdown_source, destination / "SKILL.md")
    shutil.copytree(skill_dir_path, overlay_root / skill_dir_path.name)
    return str(overlay_root), "\n".join(merged_skills)


def _skill_names(skills: str) -> list[str]:
    return [line.strip() for line in skills.splitlines() if line.strip()]


def _run_single_task_once(
    task: dict,
    model: str,
    backend: BaseAgent,
    output_root: Path,
    lobster: dict | None = None,
    thinking: str | None = None,
    models_config: dict | None = None,
    skill_dir: str | None = None,
) -> dict:
    """
    Execute a single task, returning a {"task_id", "scores", "error"} dict.
    Thread-safe: each task has its own container name and log directory.

    lobster: optional dict with keys "name", "workspace", "env".
    """
    if skill_dir is not None:
        task = dict(task)
        task["skills_path"], task["skills"] = merge_skill_dir_override(
            task.get("skills", ""),
            task.get("skills_path", ""),
            skill_dir,
        )
        logger.info(
            "[%s] CoEvo skill injection merged skills: %s",
            task["task_id"],
            task["skills"].replace("\n", ", "),
        )

    judge_env = resolve_judge_env(models_config, model)

    task_id_ori     = task["task_id"]
    workspace_path  = task["workspace_path"]
    prompt          = task["prompt"]
    timeout_seconds = task["timeout_seconds"]
    system_prompt = (
        f"You are an expert in a restricted, non-interactive environment. Solve the task efficiently before the timeout ({timeout_seconds}s). "
        "Run all processes in the foreground without user input or background services. "
        "Provide a complete, functional solution in a single pass with no placeholders.\n\n"
        f"{build_skill_read_prompt(task.get('skills', ''))}"
    )
    prompt = system_prompt + prompt

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    run_id = uuid.uuid4().hex[:6]
    _m = re.match(r"(\d+)_.*?(task_\d+)", task_id_ori)
    short_task_id = f"{_m.group(1)}_{_m.group(2)}" if _m else task_id_ori
    short_model = re.sub(r'[^a-zA-Z0-9.\-_]', '_', model.rsplit('/', 1)[-1])
    lobster_prefix = f"{lobster['name']}_" if lobster else ""
    suffix = f"{lobster_prefix}{short_model}_{timestamp}_{run_id}"
    task_id = f"{short_task_id}_{lobster_prefix}{short_model}_{timestamp}_{run_id}"

    output_dir = output_root / task["category"] / f"{task_id_ori}" / f"{suffix}"
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {"task_id": task_id, "scores": {}, "error": None, "output_dir": str(output_dir)}

    gateway_proc = None
    agent_proc = None
    elapsed_time = float(timeout_seconds)

    try:
        execution = backend.run_task(
            AgentTaskSpec(
                task_id=task_id,
                task=task,
                workspace_path=workspace_path,
                prompt=prompt,
                timeout_seconds=timeout_seconds,
                output_dir=output_dir,
                model=model,
                thinking=thinking,
                models_config=models_config,
                lobster=lobster,
                direct_env=judge_env,
            )
        )
        gateway_proc = execution.gateway_proc
        agent_proc = execution.agent_proc
        elapsed_time = execution.elapsed_time
        if execution.error:
            result["error"] = execution.error
    except Exception as exc:
        result["error"] = str(exc)
        logger.error("[%s] Unexpected backend error: %s", task_id, exc)

    finally:
        grading_transcript_path = backend.transcript_container_path
        grade_on_error = isinstance(backend, (CodexAgent, ClaudeCodeAgent))
        should_grade = task.get("automated_checks") and (
            not result.get("error") or grade_on_error
        )
        if should_grade:
            try:
                grading_transcript_path = backend.prepare_grading_transcript(task_id)
            except Exception as exc:
                logger.warning(
                    "[%s] Failed to prepare grading transcript, fallback to %s: %s",
                    task_id,
                    grading_transcript_path,
                    exc,
                )

        result = grade_the_task(
            task_id,
            workspace_path,
            output_dir,
            task,
            result,
            lobster.get("env") if lobster else None,
            transcript_container_path=grading_transcript_path,
            grade_on_error=grade_on_error,
            write_error_score_on_failure=grade_on_error,
        )
        usage = backend.collect_usage(
            task_id=task_id,
            output_dir=output_dir,
            elapsed_time=elapsed_time,
        )
        result = save_usage(output_dir, result, usage, task_id)

        try:
            collect_task_output(
                task_id,
                output_dir,
                include_workspace_changes=isinstance(backend, (CodexAgent, ClaudeCodeAgent)),
            )
        except Exception as exc:
            logger.warning("[%s] Failed to collect task output: %s", task_id, exc)

        if gateway_proc is not None:
            try:
                gateway_proc.terminate()
            except Exception:
                pass
        elif backend.expects_gateway:
            logger.warning("[%s] Gateway not started, task incomplete - likely missing required result files, check %s", task_id, output_dir)

        for _proc in [gateway_proc, agent_proc]:
            if _proc is not None:
                try:
                    close_proc_log(_proc)
                except Exception:
                    pass

        remove_container(task_id)
        logger.info("[%s] Container cleaned up", task_id)

    return result


def run_single_task(
    task: dict,
    model: str,
    backend: BaseAgent,
    output_root: Path,
    lobster: dict | None = None,
    thinking: str | None = None,
    models_config: dict | None = None,
    skill_dir: str | None = None,
    rate_limit_retries: int = 0,
    rate_limit_wait_seconds: float = 0,
) -> dict:
    attempts: list[dict] = []
    max_attempts = max(1, rate_limit_retries + 1)

    for attempt_index in range(max_attempts):
        result = _run_single_task_once(
            task,
            model,
            backend,
            output_root,
            lobster=lobster,
            thinking=thinking,
            models_config=models_config,
            skill_dir=skill_dir,
        )
        signal_path = detect_rate_limit_signal(Path(result["output_dir"]))
        if signal_path is None:
            if attempts:
                result["rate_limit_retry_attempts"] = attempts
            return result

        result["rate_limited"] = True
        result["rate_limit_signal_path"] = signal_path
        attempts.append(
            {
                "task_id": result.get("task_id"),
                "output_dir": result.get("output_dir"),
                "signal_path": signal_path,
            }
        )

        remaining = max_attempts - attempt_index - 1
        if remaining <= 0:
            result["error"] = (
                f"retry condition matched after {max_attempts} attempt(s); "
                f"last signal: {signal_path}"
            )
            result["rate_limit_retry_attempts"] = attempts
            return result

        logger.warning(
            "[%s] Retry condition matched in %s; retrying in %.1fs (%d retries left)",
            task.get("task_id", "<unknown>"),
            signal_path,
            rate_limit_wait_seconds,
            remaining,
        )
        if rate_limit_wait_seconds > 0:
            time.sleep(rate_limit_wait_seconds)

    raise RuntimeError("unreachable retry state")


def main() -> None:
    args = parse_run_batch_args(
        default_model=DEFAULT_MODEL,
        default_parallel=DEFAULT_PARALLEL,
        default_rate_limit_retries=DEFAULT_RATE_LIMIT_RETRIES,
        default_rate_limit_wait_seconds=DEFAULT_RATE_LIMIT_WAIT_SECONDS,
    )
    if args.agent_backend == "claudecode":
        backend: BaseAgent = ClaudeCodeAgent(
            anthropic_api_key=OPENROUTER_API_KEY,
            openrouter_base_url=OPENROUTER_BASE_URL_CLAUDECODE
        )
    elif args.agent_backend == "codex":
        backend = CodexAgent()
    elif args.agent_backend == "hermesagent":
        from src.agents.hermesagent import HermesAgentAgent
        backend = HermesAgentAgent(
            openrouter_api_key=OPENROUTER_API_KEY,
            openrouter_base_url=OPENROUTER_BASE_URL_OPENCLAW,
        )
    else:
        backend = OpenClawAgent(
            gateway_port=GATEWAY_PORT,
            openrouter_api_key=OPENROUTER_API_KEY,
            openrouter_base_url=OPENROUTER_BASE_URL_OPENCLAW,
            image_model=args.openclaw_image_model,
        )
    output_root = resolve_output_root(OUTPUT_DIR, args.agent_backend)
    models_config = None
    if args.models_config:
        models_config_path = Path(args.models_config).expanduser()
        if not models_config_path.is_file():
            logger.error("Models config not found: %s", models_config_path)
            sys.exit(1)
        try:
            models_config = load_models_config(models_config_path.resolve())
        except (ValueError, json.JSONDecodeError) as exc:
            logger.error("Invalid models config: %s", exc)
            sys.exit(1)

    lobster = None
    if args.lobster_workspace:
        if not args.lobster_name:
            logger.error("--lobster-workspace requires --lobster-name")
            sys.exit(1)
        workspace = Path(args.lobster_workspace).expanduser()
        if not workspace.is_dir():
            logger.error("Lobster workspace not found: %s", workspace)
            sys.exit(1)
        env_keys = [k.strip() for k in args.lobster_env.split(",") if k.strip()] if args.lobster_env else []
        lobster = {
            "name": args.lobster_name,
            "workspace": str(workspace.resolve()),
            "env": env_keys,
        }
        logger.info("Lobster mode: %s (workspace=%s, env_keys=%s)",
                     lobster["name"], lobster["workspace"], lobster["env"])

    if args.task:
        task_file = Path(args.task)
        if not task_file.exists():
            logger.error("File not found: %s", task_file)
            sys.exit(1)
        task = parse_task_md(task_file)
        logger.info("Single task mode: %s", task["task_id"])
        run_single_task(
            task,
            args.model,
            backend=backend,
            output_root=output_root,
            lobster=lobster,
            models_config=models_config,
            thinking=args.thinking,
            skill_dir=args.skill_dir,
            rate_limit_retries=args.rate_limit_retries,
            rate_limit_wait_seconds=args.rate_limit_wait_seconds,
        )
        return
    if args.category.lower() == "all":
        categories = ALL_CATEGORIES
    else:
        categories = [args.category]

    all_results: list[dict] = []
    safe_model_name = re.sub(r'[^a-zA-Z0-9.\-_]', '_', args.model)

    for category in categories:
        category_dir = TASKS_DIR / category
        if not category_dir.exists():
            logger.error("Category directory not found: %s", category_dir)
            continue

        task_files = sorted(category_dir.glob("*task_*.md"))
        if not task_files:
            logger.error("No task_*.md files found in: %s", category_dir)
            continue

        logger.info("Category: %s, %d tasks, parallelism: %d",
                    category, len(task_files), args.parallel)

        tasks = []
        for tf in task_files:
            try:
                tasks.append(parse_task_md(tf))
            except Exception as exc:
                logger.error("Parse failed %s: %s", tf, exc)

        if not tasks:
            continue

        if args.resume_skip_existing:
            tasks, skipped_tasks = partition_tasks_by_existing_runs(tasks, output_root)
            for task, runs in skipped_tasks:
                logger.info(
                    "[%s] Resume skip existing output (%d run(s), latest: %s)",
                    task["task_id"],
                    len(runs),
                    runs[-1],
                )

        if not tasks:
            logger.info("No pending tasks for category %s", category)
            continue

        results: list[dict] = []
        if args.parallel <= 1:
            for task in tasks:
                results.append(
                    run_single_task(
                        task,
                        args.model,
                        backend=backend,
                        output_root=output_root,
                        lobster=lobster,
                        models_config=models_config,
                        thinking=args.thinking,
                        skill_dir=args.skill_dir,
                        rate_limit_retries=args.rate_limit_retries,
                        rate_limit_wait_seconds=args.rate_limit_wait_seconds,
                    )
                )
        else:
            with ThreadPoolExecutor(max_workers=args.parallel) as pool:
                futures = {
                    pool.submit(
                        run_single_task,
                        task,
                        args.model,
                        backend,
                        output_root,
                        lobster,
                        args.thinking,
                        models_config,
                        args.skill_dir,
                        args.rate_limit_retries,
                        args.rate_limit_wait_seconds,
                    ): task["task_id"]
                    for task in tasks
                }
                for future in as_completed(futures):
                    tid = futures[future]
                    try:
                        results.append(future.result())
                    except Exception as exc:
                        logger.error("[%s] Thread exception: %s", tid, exc)
                        results.append({"task_id": tid, "scores": {}, "error": str(exc)})

        summary_label = f"{lobster['name']}_{safe_model_name}" if lobster else safe_model_name
        print_summary(results, category, output_root, summary_label)
        all_results.extend(results)

    if len(categories) > 1 and all_results:
        summary_label = f"{lobster['name']}_{safe_model_name}" if lobster else safe_model_name
        print_global_summary(all_results, output_root, summary_label)

if __name__ == "__main__":
    main()

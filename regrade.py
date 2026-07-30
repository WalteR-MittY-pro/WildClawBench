#!/usr/bin/env python3
"""Re-grade an already-completed task run inside a fresh container.

Reuses the agent's task_output/ (already-written results.md) without
re-running the agent. Only the judge scoring is redone.

Usage:
    python3 regrade.py <task_md_path> <run_dir>

Example:
    python3 regrade.py tasks/04_Search_Retrieval/04_Search_Retrieval_task_10_tomllib_trace.md \
        output/04_Search_Retrieval/04_Search_Retrieval_task_10_tomllib_trace/GLM-5.1_20260728_0917_f5cd63
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    task_md = Path(sys.argv[1]).resolve()
    run_dir = Path(sys.argv[2]).resolve()

    # Locate the agent's results.md inside task_output/
    candidates = list((run_dir / "task_output").rglob("results.md"))
    if not candidates:
        sys.exit(f"results.md not found under {run_dir / 'task_output'}")
    src_results = candidates[0]

    # Extract the ```python grade() block from the task.md
    text = task_md.read_text(encoding="utf-8")
    m = re.search(r"```python\s*\n(.*?)\n```", text, re.DOTALL)
    if not m:
        sys.exit("No ```python block in task.md")
    grade_code = m.group(1)

    # Build an in-container runner that calls grade()
    runner = (
        "import json, sys\n"
        "from pathlib import Path\n"
        "results_md = Path('/tmp_workspace/results/results.md')\n"
        "print('[regrade] results.md exists:', results_md.exists(), "
        "file=sys.stderr)\n"
        "if results_md.exists():\n"
        "    print('[regrade] preview:', results_md.read_text()[:120], "
        "file=sys.stderr)\n"
        f"{grade_code}\n\n"
        "scores = grade(transcript='', workspace_path='/tmp_workspace')\n"
        "print(json.dumps(scores, ensure_ascii=False))\n"
    )

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(runner)
        runner_host = f.name

    container = "regrade_tmp"
    # Cleanup any stale container, then start a fresh one
    subprocess.run(["docker", "rm", "-f", container],
                   capture_output=True, text=True)

    print(f"[regrade] task={task_md.name}")
    print(f"[regrade] run={run_dir}")
    print(f"[regrade] source results.md = {src_results}")
    print(f"[regrade] judge = "
          f"{os.environ.get('JUDGE_MODEL')} @ "
          f"{os.environ.get('OPENROUTER_BASE_URL')}")
    print()

    docker_image = os.environ.get("DOCKER_IMAGE", "wildclawbench-ubuntu:v1.3")

    # Start container with judge env injected.
    # IMPORTANT: clear proxy env vars (the image hardcodes an unreachable proxy).
    env_args = []
    for key in ("OPENROUTER_API_KEY", "OPENROUTER_BASE_URL", "JUDGE_MODEL"):
        val = os.environ.get(key, "")
        env_args += ["-e", f"{key}={val}"]
    # Override image's hardcoded proxy settings
    env_args += [
        "-e", "http_proxy=",
        "-e", "https_proxy=",
        "-e", "HTTP_PROXY=",
        "-e", "HTTPS_PROXY=",
        "-e", "no_proxy=*",
    ]

    cmd = ["docker", "run", "-d", "--name", container,
           *env_args, "-v", f"{runner_host}:/tmp/_grade.py",
           "--entrypoint", "/bin/bash", docker_image,
           "-c", "mkdir -p /tmp_workspace/results && "
           "touch /tmp_workspace/results/results.md && "
           "tail -f /dev/null"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"Container start failed:\n{r.stderr}")
    # Wait until the container is actually running and the dir is ready.
    import time
    for _ in range(20):
        chk = subprocess.run(
            ["docker", "exec", container, "test", "-d", "/tmp_workspace/results"],
            capture_output=True, text=True,
        )
        if chk.returncode == 0:
            break
        time.sleep(0.5)
    else:
        sys.exit("Container started but /tmp_workspace/results never appeared")

    # Copy the agent's results.md into the container's expected path
    r = subprocess.run(
        ["docker", "cp", str(src_results), f"{container}:/tmp_workspace/results/results.md"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        sys.exit(f"docker cp results.md failed:\n{r.stderr}")

    # Copy the grader into the container and run it
    subprocess.run(
        ["docker", "cp", runner_host, f"{container}:/tmp/_grade.py"],
        capture_output=True, text=True,
    )

    print("[regrade] running grader in container...")
    r = subprocess.run(
        ["docker", "exec", "-e", "OPENROUTER_API_KEY=" + os.environ.get("OPENROUTER_API_KEY", ""),
         "-e", "OPENROUTER_BASE_URL=" + os.environ.get("OPENROUTER_BASE_URL", ""),
         "-e", "JUDGE_MODEL=" + os.environ.get("JUDGE_MODEL", ""),
         container, "python3", "/tmp/_grade.py"],
        capture_output=True, text=True, timeout=180,
    )

    Path(runner_host).unlink(missing_ok=True)
    subprocess.run(["docker", "rm", "-f", container], capture_output=True)

    print("\n=== STDERR ===")
    print(r.stderr[-2000:] if r.stderr else "(empty)")
    print("\n=== STDOUT (scores) ===")
    print(r.stdout or "(empty)")

    # Persist score.json
    out = run_dir / "score.json"
    if r.stdout.strip():
        try:
            import json
            scores = json.loads(r.stdout.strip().splitlines()[-1])
            out.write_text(json.dumps(scores, indent=2, ensure_ascii=False),
                           encoding="utf-8")
            print(f"\n[regrade] written -> {out}")
        except Exception as exc:
            print(f"\n[regrade] could not parse scores JSON: {exc}")


if __name__ == "__main__":
    main()

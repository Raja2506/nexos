# backend/app/agents/sandbox_executor.py
import subprocess
import sys
import tempfile
from pathlib import Path

FORBIDDEN_KEYWORDS = [
    "import os", "import sys", "import subprocess", "import shutil",
    "open(", "eval(", "exec(", "__import__", "socket", "requests",
]


class SandboxExecutionError(Exception):
    pass


def run_code_safely(code: str, timeout_seconds: int = 5) -> str:
    """
    Runs untrusted Python code in a separate process with a timeout.
    Blocks obviously dangerous patterns before execution as a first line
    of defense (not foolproof, but stops naive mistakes).
    """
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in code:
            raise SandboxExecutionError(f"Blocked: code contains forbidden pattern '{keyword}'")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp_path = Path(tmp.name)

    try:
        result = subprocess.run(
            [sys.executable, str(tmp_path)],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        if result.returncode != 0:
            raise SandboxExecutionError(f"Execution failed:\n{result.stderr}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise SandboxExecutionError(f"Code timed out after {timeout_seconds}s (possible infinite loop)")
    finally:
        tmp_path.unlink(missing_ok=True)  # always clean up the temp file
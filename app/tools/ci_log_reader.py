from __future__ import annotations

from pathlib import Path

from app.tools.path_guard import resolve_under_root
from app.tools.redactor import redact_secrets


def read_ci_log(root: Path | str, log_path: Path | str = "ci.log") -> list[dict[str, str | int]]:
    safe_path = resolve_under_root(root, log_path)
    content = redact_secrets(safe_path.read_text(encoding="utf-8"))
    return [{"line": index, "content": line} for index, line in enumerate(content.splitlines(), start=1)]

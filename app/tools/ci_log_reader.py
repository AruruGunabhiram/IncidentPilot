"""Deterministic CI log reader.

Reads a CI log from disk *inside the allowed root only*, redacts secrets before
anything else touches the text, and returns the lines with their original
1-based line numbers preserved so later evidence can cite exact locations.
"""

from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from app.tools.path_guard import resolve_under_root
from app.tools.redactor import redact_with_count


class LogLine(TypedDict):
    line: int
    content: str


class CiLogResult(TypedDict):
    path: str
    line_count: int
    redactions_applied: int
    lines: list[LogLine]


def read_ci_log(root: Path | str, log_path: Path | str = "ci.log") -> list[LogLine]:
    """Return redacted log lines as ``{"line": n, "content": ...}``.

    Line numbers are 1-based and match the original file. Raises
    ``UnsafePathError`` if ``log_path`` escapes ``root`` and ``FileNotFoundError``
    if the resolved file does not exist.
    """
    return read_ci_log_structured(root, log_path)["lines"]


def read_ci_log_structured(
    root: Path | str, log_path: Path | str = "ci.log"
) -> CiLogResult:
    """Return a structured, agent-friendly view of a redacted CI log.

    Includes the resolved relative path, line count, number of redactions
    applied, and the redacted lines with preserved line numbers.
    """
    safe_path = resolve_under_root(root, log_path)
    if not safe_path.is_file():
        raise FileNotFoundError(f"CI log not found under root: {log_path}")

    redacted, redactions = redact_with_count(safe_path.read_text(encoding="utf-8"))
    lines: list[LogLine] = [
        {"line": index, "content": content}
        for index, content in enumerate(redacted.splitlines(), start=1)
    ]

    root_path = Path(root).resolve()
    try:
        rel_path = str(safe_path.relative_to(root_path))
    except ValueError:
        rel_path = str(safe_path)

    return {
        "path": rel_path,
        "line_count": len(lines),
        "redactions_applied": redactions,
        "lines": lines,
    }

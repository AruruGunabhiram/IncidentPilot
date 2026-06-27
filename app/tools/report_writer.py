"""Deterministic incident report serializer.

Turns an :class:`~app.schemas.report.IncidentReport` (or a plain dict with the
same shape) into JSON and Markdown. Every string value is passed through the
redactor first, so no raw secret can appear in either output even if upstream
evidence accidentally carried one. Output is deterministic for a given input.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypedDict

from app.tools.redactor import redact_secrets

JSON_FILENAME = "report.json"
MARKDOWN_FILENAME = "report.md"


class WrittenReport(TypedDict):
    json_path: str
    markdown_path: str


def _to_plain_dict(report: Any) -> dict[str, Any]:
    """Normalize a report into a JSON-safe dict.

    Accepts a Pydantic model (``model_dump``) or an already-plain dict.
    """
    if hasattr(report, "model_dump"):
        return report.model_dump(mode="json")
    if isinstance(report, dict):
        # Round-trip through json to coerce any non-JSON-native values
        # (e.g. datetimes) deterministically.
        return json.loads(json.dumps(report, default=str))
    raise TypeError("report must be a Pydantic model or a dict")


def _redact_tree(value: Any) -> Any:
    """Recursively redact every string in a nested JSON-like structure."""
    if isinstance(value, str):
        return redact_secrets(value)
    if isinstance(value, dict):
        return {key: _redact_tree(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_tree(item) for item in value]
    return value


def build_report_dict(report: Any) -> dict[str, Any]:
    """Return a fully redacted, JSON-safe dict for ``report``."""
    return _redact_tree(_to_plain_dict(report))


def render_json(report: Any) -> str:
    """Return a deterministic, redacted JSON string for ``report``."""
    return json.dumps(build_report_dict(report), indent=2, ensure_ascii=False)


def _evidence_line(item: dict[str, Any]) -> str:
    path = item.get("path") or item.get("source") or "unknown"
    start = item.get("line_start")
    end = item.get("line_end")
    if start is not None and end is not None and start != end:
        location = f"{path}:{start}-{end}"
    elif start is not None:
        location = f"{path}:{start}"
    else:
        location = str(path)
    summary = item.get("summary", "")
    snippet = item.get("snippet")
    line = f"- `{location}` — {summary}".rstrip(" —")
    if snippet:
        line += f"\n  - `{snippet}`"
    return line


def render_markdown(report: Any) -> str:
    """Return a deterministic, redacted Markdown report for ``report``."""
    data = build_report_dict(report)

    title = data.get("title") or data.get("incident_id") or "Incident Report"
    lines: list[str] = [f"# {title}", ""]

    meta = [
        ("Incident ID", data.get("incident_id")),
        ("Severity", data.get("severity")),
        ("Affected service", data.get("affected_service")),
        ("Status", data.get("status")),
        ("Confidence", data.get("confidence")),
        ("Needs human review", data.get("needs_human_review")),
    ]
    for label, value in meta:
        if value is not None:
            lines.append(f"- **{label}:** {value}")
    lines.append("")

    if data.get("summary"):
        lines += ["## Summary", "", str(data["summary"]), ""]

    if data.get("primary_error"):
        lines += ["## Primary error", "", f"`{data['primary_error']}`", ""]

    blocked = data.get("blocked_reasons") or []
    if blocked:
        lines += ["## Blocked reasons", ""]
        lines += [f"- {reason}" for reason in blocked]
        lines.append("")

    evidence = data.get("evidence") or []
    if evidence:
        lines += ["## Evidence", ""]
        lines += [_evidence_line(item) for item in evidence]
        lines.append("")

    root_cause = data.get("root_cause") or {}
    if root_cause.get("summary"):
        lines += ["## Root-cause hypothesis", ""]
        category = root_cause.get("category")
        if category:
            lines.append(f"- **Category:** {category}")
        lines += ["", str(root_cause["summary"]), ""]

    fix_plan = data.get("fix_plan") or {}
    if fix_plan:
        steps = fix_plan.get("steps") or []
        regression = fix_plan.get("regression_tests") or []
        if fix_plan.get("summary") or steps:
            lines += ["## Fix plan", ""]
            if fix_plan.get("summary"):
                lines += [str(fix_plan["summary"]), ""]
            if steps:
                lines += [f"{i}. {step}" for i, step in enumerate(steps, start=1)]
                lines.append("")
            if regression:
                lines += ["**Regression tests:**", ""]
                lines += [f"- {test}" for test in regression]
                lines.append("")

    safety = data.get("safety_review") or {}
    if safety:
        lines += ["## Safety review", ""]
        safety_meta = [
            ("Approved for display", safety.get("approved_for_display")),
            ("Approved for GitHub issue", safety.get("approved_for_github_issue")),
            ("Risk level", safety.get("risk_level")),
            ("Human approval required", safety.get("human_approval_required")),
            ("Required human action", safety.get("required_human_action")),
        ]
        for label, value in safety_meta:
            if value is not None:
                lines.append(f"- **{label}:** {value}")
        lines.append("")

    # Single trailing newline, no trailing whitespace lines.
    return "\n".join(lines).rstrip() + "\n"


def write_report(report: Any, output_dir: Path | str) -> WrittenReport:
    """Write redacted ``report.json`` and ``report.md`` into ``output_dir``.

    Returns the two written paths. Creates ``output_dir`` if needed.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    json_path = out / JSON_FILENAME
    markdown_path = out / MARKDOWN_FILENAME
    json_path.write_text(render_json(report) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")

    return {"json_path": str(json_path), "markdown_path": str(markdown_path)}

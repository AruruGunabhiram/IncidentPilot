from __future__ import annotations

from pathlib import Path

from app.tools.path_guard import resolve_under_root


def search_repo(term: str, repo_root: Path | str, max_results: int = 25) -> list[dict[str, str | int]]:
    if not term:
        return []

    root = Path(repo_root).resolve()
    results: list[dict[str, str | int]] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part.startswith(".") for part in path.relative_to(root).parts):
            continue

        safe_path = resolve_under_root(root, path.relative_to(root))
        try:
            lines = safe_path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        for line_number, line in enumerate(lines, start=1):
            if term.lower() in line.lower():
                results.append(
                    {
                        "path": str(safe_path.relative_to(root)),
                        "line": line_number,
                        "snippet": line.strip(),
                    }
                )
                if len(results) >= max_results:
                    return results

    return results

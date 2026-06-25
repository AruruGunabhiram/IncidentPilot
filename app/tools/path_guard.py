from __future__ import annotations

from pathlib import Path


class UnsafePathError(ValueError):
    """Raised when a requested path escapes the allowed root."""


def resolve_under_root(root: Path | str, requested_path: Path | str) -> Path:
    requested = Path(requested_path)
    if ".." in requested.parts:
        raise UnsafePathError("Path traversal is not allowed")

    root_path = Path(root).resolve()
    candidate = (root_path / requested).resolve() if not requested.is_absolute() else requested.resolve()

    if candidate != root_path and root_path not in candidate.parents:
        raise UnsafePathError("Path must stay under the allowed root")

    return candidate

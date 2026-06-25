from pathlib import Path

import pytest

from app.tools.path_guard import UnsafePathError, resolve_under_root


def test_path_guard_blocks_traversal():
    with pytest.raises(UnsafePathError):
        resolve_under_root(Path("demo/demo_repo"), "../../etc/passwd")

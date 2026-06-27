from pathlib import Path

import pytest

from app.tools.path_guard import UnsafePathError, resolve_under_root

ROOT = Path("demo/demo_repo")


# ---- happy paths -----------------------------------------------------------


def test_resolves_relative_path_under_root():
    resolved = resolve_under_root(ROOT, "app/routes/payments.py")
    assert resolved == (ROOT / "app/routes/payments.py").resolve()
    assert resolved.is_file()


def test_root_itself_is_allowed():
    resolved = resolve_under_root(ROOT, ".")
    assert resolved == ROOT.resolve()


# ---- failure paths ---------------------------------------------------------


def test_path_guard_blocks_traversal():
    with pytest.raises(UnsafePathError):
        resolve_under_root(ROOT, "../../etc/passwd")


def test_path_guard_blocks_absolute_escape():
    with pytest.raises(UnsafePathError):
        resolve_under_root(ROOT, "/etc/passwd")


def test_path_guard_blocks_sneaky_parent_segment():
    with pytest.raises(UnsafePathError):
        resolve_under_root(ROOT, "app/../../secrets.txt")

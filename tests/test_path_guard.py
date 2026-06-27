from pathlib import Path

import pytest

from app.tools.path_guard import (
    PathGuardError,
    resolve_safe_path,
    verify_directory_exists,
    verify_file_exists,
)


@pytest.fixture()
def root(tmp_path: Path) -> Path:
    """An allowed root directory with one nested file."""
    base = tmp_path / "repo"
    (base / "app" / "routes").mkdir(parents=True)
    (base / "app" / "routes" / "payments.py").write_text("ok", encoding="utf-8")
    (base / "top.txt").write_text("ok", encoding="utf-8")
    return base


# 1. Allows a normal file inside the root. -----------------------------------
def test_allows_normal_file_inside_root(root: Path):
    resolved = resolve_safe_path(root, "top.txt")
    assert resolved == (root / "top.txt").resolve()


# 2. Blocks "../outside.txt". -------------------------------------------------
def test_blocks_single_parent_traversal(root: Path):
    with pytest.raises(PathGuardError):
        resolve_safe_path(root, "../outside.txt")


# 3. Blocks "../../etc/passwd". -----------------------------------------------
def test_blocks_deep_parent_traversal(root: Path):
    with pytest.raises(PathGuardError):
        resolve_safe_path(root, "../../etc/passwd")


# 4. Blocks an absolute path outside the allowed root. ------------------------
def test_blocks_absolute_path_outside_root(root: Path):
    with pytest.raises(PathGuardError):
        resolve_safe_path(root, "/etc/passwd")


# 5. Blocks a symlink that points outside the root. --------------------------
def test_blocks_symlink_escape(root: Path, tmp_path: Path):
    outside = tmp_path / "outside"
    outside.mkdir()
    secret = outside / "secret.txt"
    secret.write_text("top secret", encoding="utf-8")

    link = root / "escape.txt"
    try:
        link.symlink_to(secret)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks not supported on this platform")

    with pytest.raises(PathGuardError):
        resolve_safe_path(root, "escape.txt")


# 6. Verifies an existing file. ----------------------------------------------
def test_verify_file_exists_for_real_file(root: Path):
    resolved = verify_file_exists(root, "app/routes/payments.py")
    assert resolved.is_file()
    assert resolved == (root / "app/routes/payments.py").resolve()


# 7. Fails on a missing file. -------------------------------------------------
def test_verify_file_exists_missing_file_raises(root: Path):
    with pytest.raises(FileNotFoundError):
        verify_file_exists(root, "app/routes/missing.py")


# 8. Allows a nested valid file. ---------------------------------------------
def test_allows_nested_valid_file(root: Path):
    resolved = resolve_safe_path(root, "app/routes/payments.py")
    assert resolved == (root / "app/routes/payments.py").resolve()
    # And the directory check works for the nested directory too.
    assert verify_directory_exists(root, "app/routes").is_dir()


# 9. Returns a resolved Path object. -----------------------------------------
def test_returns_resolved_path_object(root: Path):
    resolved = resolve_safe_path(root, "top.txt")
    assert isinstance(resolved, Path)
    assert resolved.is_absolute()
    assert resolved == resolved.resolve()


# Bonus: the root itself is allowed, and a clear message is raised on escape.
def test_root_itself_is_allowed_and_error_is_readable(root: Path):
    assert verify_directory_exists(root) == root.resolve()
    with pytest.raises(PathGuardError) as excinfo:
        resolve_safe_path(root, "../../etc/passwd")
    assert "traversal" in str(excinfo.value).lower()

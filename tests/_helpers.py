"""Shared test helpers."""
import shutil
import tempfile
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def fixture_dir(name: str) -> Path:
    return FIXTURES / name


def copy_fixture(name: str) -> Path:
    """Copy a fixture job dir to a temp dir so generator tests don't mutate fixtures."""
    src = fixture_dir(name)
    tmp = Path(tempfile.mkdtemp(prefix="mqai_fix_"))
    dest = tmp / name
    shutil.copytree(src, dest)
    return dest

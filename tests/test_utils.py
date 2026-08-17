import pytest
from pathlib import Path
from utils import format_size, validate_path

def test_format_size_units():
    assert format_size(500) == "500.00 B"
    assert format_size(1024) == "1.00 KB"
    assert format_size(1024 * 1024) == "1.00 MB"
    assert format_size(1024 * 1024 * 1024) == "1.00 GB"

def test_format_size_negative():
    with pytest.raises(ValueError):
        format_size(-10)

def test_validate_path_valid(dummy_dir: Path):
    resolved = validate_path(str(dummy_dir))
    assert resolved == dummy_dir.resolve()

def test_validate_path_nonexistent(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        validate_path(str(tmp_path / "nonexistent_dir"))

def test_validate_path_not_a_directory(dummy_dir: Path):
    file_path = dummy_dir / "notes.txt"
    with pytest.raises(NotADirectoryError):
        validate_path(str(file_path))
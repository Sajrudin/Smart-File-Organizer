import pytest
from pathlib import Path

@pytest.fixture
def dummy_dir(tmp_path: Path) -> Path:
    """
    Creates a temporary directory with various files across subfolders:
    - nested/photo.jpg (Images)
    - notes.txt (Documents)
    - script.py (Code)
    - song.mp3 (Music)
    - ignored .git folder
    """
    base = tmp_path / "test_workspace"
    base.mkdir()

    # Regular files
    (base / "notes.txt").write_text("Meeting notes content", encoding="utf-8")
    (base / "script.py").write_text("print('hello')", encoding="utf-8")
    (base / "song.mp3").write_bytes(b"dummy mp3 audio data")

    # Subdirectory with an image
    nested_dir = base / "subfolder"
    nested_dir.mkdir()
    (nested_dir / "photo.jpg").write_bytes(b"\xff\xd8\xff dummy jpeg")

    # Ignored directory
    git_dir = base / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_text("git config content", encoding="utf-8")

    # Exact duplicates (same bytes)
    (base / "doc1.txt").write_text("Identical duplicate content here.", encoding="utf-8")
    (base / "copy_doc1.txt").write_text("Identical duplicate content here.", encoding="utf-8")

    # Non-duplicates (different content)
    (base / "photo1.jpg").write_bytes(b"\xff\xd8\xff Unique image one")
    (base / "photo2.jpg").write_bytes(b"\xff\xd8\xff Unique image two")

    # Empty 0-byte file
    (base / "empty.txt").write_text("", encoding="utf-8")

    # Search & pattern test files
    (base / "data_2026_01.csv").write_text("col1,col2\n1,2", encoding="utf-8")
    (base / "data_2026_02.csv").write_text("col1,col2\n3,4", encoding="utf-8")

    return base
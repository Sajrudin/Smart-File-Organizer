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

    return base
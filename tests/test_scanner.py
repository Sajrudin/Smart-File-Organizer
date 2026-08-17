from pathlib import Path
from scanner import scan_directory, get_file_category

def test_get_file_category():
    assert get_file_category(".jpg") == "Images"
    assert get_file_category(".PNG") == "Images"
    assert get_file_category(".pdf") == "Documents"
    assert get_file_category(".xyz123") == "Others"
    assert get_file_category(".py") == "Code"
    assert get_file_category(".mp3") == "Music"
    assert get_file_category(".mp4") == "Videos"

def test_scan_directory(dummy_dir: Path):
    result = scan_directory(dummy_dir)

    # 4 files total (notes.txt, script.py, song.mp3, photo.jpg), .git/config must be skipped
    assert result.total_files == 4
    assert result.total_size_bytes > 0
    assert result.category_counts.get("Documents") == 1
    assert result.category_counts.get("Images") == 1
    assert result.category_counts.get("Code") == 1
    assert result.category_counts.get("Music") == 1
    assert ".git" not in [f.name for f in result.files]
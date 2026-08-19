from pathlib import Path
from scanner import scan_directory
from search import search_files, search_by_substring, search_by_glob, search_by_regex


def test_search_substring(dummy_dir: Path):
    scan_result = scan_directory(dummy_dir)

    results = search_by_substring(scan_result.files, "doc1")
    assert len(results) == 2
    assert {f.name for f in results} == {"doc1.txt", "copy_doc1.txt"}


def test_search_glob(dummy_dir: Path):
    scan_result = scan_directory(dummy_dir)

    # Match all CSV files
    csv_results = search_by_glob(scan_result.files, "*.csv")
    assert len(csv_results) == 2

    # Match wildcards with 'photo?.jpg' (photo1.jpg, photo2.jpg)
    photo_results = search_by_glob(scan_result.files, "photo?.jpg")
    assert len(photo_results) == 2


def test_search_regex(dummy_dir: Path):
    scan_result = scan_directory(dummy_dir)

    # Regex matching 'data_2026_\d{2}\.csv'
    regex_results = search_by_regex(scan_result.files, r"^data_2026_\d{2}\.csv$")
    assert len(regex_results) == 2


def test_search_with_category_filter(dummy_dir: Path):
    scan_result = scan_directory(dummy_dir)

    # Search for 'photo' strictly within Documents (should find 0)
    results = search_files(
        scan_result.files,
        query="photo",
        search_type="substring",
        category_filter="Documents",
    )
    assert len(results) == 0

    # Search for 'photo' within Images (should find 3: photo.jpg, photo1.jpg, photo2.jpg)
    results_img = search_files(
        scan_result.files,
        query="photo",
        search_type="substring",
        category_filter="Images",
    )
    assert len(results_img) == 3
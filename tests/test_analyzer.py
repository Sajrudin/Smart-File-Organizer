from pathlib import Path
from scanner import scan_directory
from analyzer import analyze_storage, get_category_percentages

def test_storage_analysis(dummy_dir: Path):
    scan_result = scan_directory(dummy_dir)
    analysis = analyze_storage(scan_result, top_n=2)

    assert analysis["total_files"] == 11
    assert len(analysis["largest_files"]) == 2
    # Verify sorted descending by bytes
    assert analysis["largest_files"][0].size_bytes >= analysis["largest_files"][1].size_bytes

def test_empty_directory_analysis(tmp_path: Path):
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    scan_result = scan_directory(empty_dir)
    
    analysis = analyze_storage(scan_result)
    assert analysis["total_files"] == 0
    assert analysis["total_size_bytes"] == 0
    assert get_category_percentages({}, 0) == {}
import json
from pathlib import Path
from analyzer import analyze_storage
from reporter import generate_json_report, generate_text_report
from scanner import scan_directory


def test_generate_text_report(dummy_dir: Path):
    # Step 1: Scan and analyze directory
    scan_result = scan_directory(dummy_dir)
    analysis_data = analyze_storage(scan_result)

    # Step 2: Generate text report
    report_path = generate_text_report(scan_result, analysis_data)

    # Assertions on file creation
    assert report_path.exists()
    assert report_path.suffix == ".txt"

    content = report_path.read_text(encoding="utf-8")

    # Verify key sections and content exist in the text file
    assert "SMART FILE ORGANIZER & STORAGE REPORT" in content
    assert str(scan_result.root_path) in content
    assert "Total Files Found   : 11" in content
    assert "STORAGE DISTRIBUTION BY CATEGORY:" in content
    assert "TOP LARGEST FILES:" in content
    assert "Documents" in content
    assert "Images" in content


def test_generate_json_report(dummy_dir: Path):
    # Step 1: Scan and analyze directory
    scan_result = scan_directory(dummy_dir)
    analysis_data = analyze_storage(scan_result)

    # Step 2: Generate JSON report
    report_path = generate_json_report(scan_result, analysis_data)

    # Assertions on file creation
    assert report_path.exists()
    assert report_path.suffix == ".json"

    # Step 3: Parse JSON and verify fields
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["root_path"] == str(scan_result.root_path)
    assert data["total_files"] == 11
    assert data["total_size_bytes"] == scan_result.total_size_bytes
    assert "total_size_formatted" in data
    assert "category_counts" in data
    assert "category_sizes" in data
    assert "category_percentages" in data
    assert "largest_files" in data

    # Verify largest files array contains structured objects
    assert len(data["largest_files"]) <= 10
    first_largest = data["largest_files"][0]
    assert "name" in first_largest
    assert "path" in first_largest
    assert "size_bytes" in first_largest
    assert "size_formatted" in first_largest
    assert "category" in first_largest
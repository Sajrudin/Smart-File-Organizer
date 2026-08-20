from pathlib import Path
from scanner import scan_directory
from duplicates import calculate_sha256, find_duplicates, delete_duplicate_file


def test_calculate_sha256(dummy_dir: Path):
    file1 = dummy_dir / "doc1.txt"
    file2 = dummy_dir / "copy_doc1.txt"
    file_diff = dummy_dir / "photo1.jpg"

    hash1 = calculate_sha256(file1)
    hash2 = calculate_sha256(file2)
    hash_diff = calculate_sha256(file_diff)

    assert hash1 is not None
    assert hash1 == hash2  # Identical content yields identical hash
    assert hash1 != hash_diff


def test_find_duplicates(dummy_dir: Path):
    scan_result = scan_directory(dummy_dir)
    duplicates = find_duplicates(scan_result.files)

    # Exactly 1 duplicate group should be found (doc1.txt & copy_doc1.txt)
    assert len(duplicates) == 1

    dup_files = list(duplicates.values())[0]
    assert len(dup_files) == 2
    dup_names = {f.name for f in dup_files}
    assert dup_names == {"doc1.txt", "copy_doc1.txt"}


def test_delete_duplicate_file(dummy_dir: Path):
    target = dummy_dir / "copy_doc1.txt"
    assert target.exists()

    success = delete_duplicate_file(target)
    assert success is True
    assert not target.exists()
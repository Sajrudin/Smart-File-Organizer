from pathlib import Path
from scanner import scan_directory
from organizer import organize_files, resolve_collision
from history import load_latest_transaction, rollback_transaction

def test_organize_and_rollback(dummy_dir: Path):
    # Step 1: Scan files
    scan_result = scan_directory(dummy_dir)
    assert scan_result.total_files == 11

    # Step 2: Organize files
    tx, success, fail = organize_files(dummy_dir, scan_result.files)
    assert fail == 0
    assert success == 11
    assert (dummy_dir / "Documents" / "notes.txt").exists()
    assert (dummy_dir / "Images" / "photo.jpg").exists()

    # Step 3: Verify transaction log exists
    loaded_tx, log_path = load_latest_transaction()
    assert loaded_tx is not None
    assert loaded_tx.transaction_id == tx.transaction_id
    assert len(loaded_tx.operations) == 11

    # Step 4: Test Rollback
    rb_success, rb_fail = rollback_transaction(loaded_tx, log_path)
    assert rb_fail == 0
    assert rb_success == 11
    
    # Check that files were returned to their original paths
    assert (dummy_dir / "notes.txt").exists()
    assert (dummy_dir / "subfolder" / "photo.jpg").exists()

def test_collision_resolution(tmp_path: Path):
    existing_file = tmp_path / "report.pdf"
    existing_file.write_text("first", encoding="utf-8")

    # Destination exists -> returns a new suffixed path
    new_path = resolve_collision(existing_file)
    assert new_path != existing_file
    assert "report_" in new_path.name
    assert new_path.suffix == ".pdf"
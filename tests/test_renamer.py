from pathlib import Path
from scanner import scan_directory
from search import search_by_glob
from renamer import generate_rename_plan, execute_rename_plan
from history import load_latest_transaction, rollback_transaction


def test_generate_rename_plan(dummy_dir: Path):
    scan_result = scan_directory(dummy_dir)
    csv_files = search_by_glob(scan_result.files, "*.csv")

    # Generate plan with zero-padded pattern 'Archive_###'
    plan = generate_rename_plan(csv_files, pattern="Archive_###", start_index=1)

    assert len(plan) == 2
    assert plan[0][1].name == "Archive_001.csv"
    assert plan[1][1].name == "Archive_002.csv"

    # Verify dry-run: target files must not exist yet on disk
    assert not (dummy_dir / "Archive_001.csv").exists()
    assert not (dummy_dir / "Archive_002.csv").exists()


def test_execute_rename_and_rollback(dummy_dir: Path):
    scan_result = scan_directory(dummy_dir)
    csv_files = search_by_glob(scan_result.files, "*.csv")

    # Step 1: Execute rename
    plan = generate_rename_plan(csv_files, pattern="Report_##", start_index=10)
    tx, success, fail = execute_rename_plan(plan)

    assert success == 2
    assert fail == 0
    assert (dummy_dir / "Report_10.csv").exists()
    assert (dummy_dir / "Report_11.csv").exists()

    # Step 2: Rollback transaction
    loaded_tx, log_path = load_latest_transaction()
    assert loaded_tx is not None
    assert loaded_tx.transaction_id == tx.transaction_id

    rb_success, rb_fail = rollback_transaction(loaded_tx, log_path)
    assert rb_success == 2
    assert rb_fail == 0

    # Step 3: Verify restoration to original filenames
    assert (dummy_dir / "data_2026_01.csv").exists()
    assert (dummy_dir / "data_2026_02.csv").exists()
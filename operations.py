from pathlib import Path
from typing import Any

from analyzer import analyze_storage
from duplicates import delete_duplicate_file, find_duplicates
from history import load_latest_transaction, rollback_transaction
from logger import setup_logger
from models import FileInfo, ScanResult
from organizer import organize_files
from renamer import execute_rename_plan, generate_rename_plan
from reporter import generate_json_report, generate_text_report
from scanner import scan_directory
from search import search_files
from utils import validate_path

logger = setup_logger("operations")


def run_scan(target_path_str: str) -> ScanResult:
    """Validates path and runs a full directory scan."""
    path = validate_path(target_path_str)
    return scan_directory(path)


def run_analysis(scan_result: ScanResult, top_n: int = 10) -> dict[str, Any]:
    """Runs storage analytics on an existing ScanResult."""
    return analyze_storage(scan_result, top_n=top_n)


def run_organize(target_path_str: str, scan_result: ScanResult | None = None) -> dict[str, Any]:
    """
    Scans (if needed) and organizes files into category subdirectories.
    Returns summary statistics and transaction ID.
    """
    path = validate_path(target_path_str)
    if scan_result is None or scan_result.root_path != path:
        scan_result = scan_directory(path)

    tx, success, fail = organize_files(path, scan_result.files)
    return {
        "transaction_id": tx.transaction_id,
        "successful_moves": success,
        "failed_moves": fail,
    }


def run_duplicate_detection(scan_result: ScanResult) -> dict[str, list[FileInfo]]:
    """Identifies duplicate files within a ScanResult."""
    return find_duplicates(scan_result.files)


def run_delete_duplicate(file_path: Path) -> bool:
    """Deletes a selected duplicate file from disk."""
    return delete_duplicate_file(file_path)


def run_search(
    files: list[FileInfo],
    query: str,
    search_type: str = "substring",
    category_filter: str | None = None,
) -> list[FileInfo]:
    """Filters files by substring, glob, or regex."""
    return search_files(files, query, search_type, category_filter)


def run_rename_preview(
    files: list[FileInfo], pattern: str, start_index: int = 1
) -> list[tuple[FileInfo, Path]]:
    """Generates a dry-run preview plan for batch renaming."""
    return generate_rename_plan(files, pattern, start_index)


def run_rename_execute(plan: list[tuple[FileInfo, Path]]) -> dict[str, Any]:
    """Executes a batch renaming plan and logs the transaction."""
    tx, success, fail = execute_rename_plan(plan)
    return {
        "transaction_id": tx.transaction_id,
        "successful_renames": success,
        "failed_renames": fail,
    }


def run_generate_reports(
    scan_result: ScanResult, analysis_data: dict[str, Any]
) -> tuple[Path, Path]:
    """Generates both TXT and JSON reports for the scan and analysis data."""
    txt_path = generate_text_report(scan_result, analysis_data)
    json_path = generate_json_report(scan_result, analysis_data)
    return txt_path, json_path


def run_undo() -> dict[str, Any]:
    """Loads the most recent transaction and performs a rollback."""
    transaction, log_path = load_latest_transaction()
    if not transaction or not log_path:
        return {"status": "no_history", "message": "No transaction history found to undo."}

    success, fail = rollback_transaction(transaction, log_path)
    return {
        "status": "success",
        "transaction_id": transaction.transaction_id,
        "action_type": transaction.action_type,
        "successful_restores": success,
        "failed_restores": fail,
    }
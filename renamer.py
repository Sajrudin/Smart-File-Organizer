import os
import re
from datetime import datetime
from pathlib import Path

from history import save_transaction
from logger import setup_logger
from models import FileInfo, FileMoveOperation, Transaction

logger = setup_logger("renamer")


def generate_rename_plan(
    files: list[FileInfo],
    pattern: str,
    start_index: int = 1
) -> list[tuple[FileInfo, Path]]:
    """
    Generates a dry-run preview plan without modifying files on disk.
    Pattern uses '#' for sequential padding (e.g., 'Doc_###' -> 'Doc_001.pdf').
    Returns a list of (FileInfo, new_path) tuples.
    """
    plan: list[tuple[FileInfo, Path]] = []
    
    # Count consecutive hashes for padding width (e.g., '###' -> width 3)
    match = re.search(r"#+", pattern)
    padding_width = len(match.group(0)) if match else 3

    current_num = start_index

    for file_info in files:
        extension = file_info.path.suffix
        
        if match:
            padded_number = str(current_num).zfill(padding_width)
            new_stem = pattern.replace(match.group(0), padded_number, 1)
        else:
            # If no hash is supplied, append sequential counter as fallback
            new_stem = f"{pattern}_{str(current_num).zfill(padding_width)}"

        new_filename = f"{new_stem}{extension}"
        new_path = file_info.path.parent / new_filename

        plan.append((file_info, new_path))
        current_num += 1

    return plan


def execute_rename_plan(plan: list[tuple[FileInfo, Path]]) -> tuple[Transaction, int, int]:
    """
    Executes the dry-run rename plan and persists changes into a Transaction log.
    Returns (Transaction, successful_count, failed_count).
    """
    timestamp_str = datetime.now().isoformat()
    tx_id = f"tx_rename_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    transaction = Transaction(
        transaction_id=tx_id,
        action_type="RENAME",
        timestamp=timestamp_str,
        operations=[]
    )

    success_count = 0
    fail_count = 0

    for file_info, new_path in plan:
        # Skip if the source and destination paths are identical
        if file_info.path.resolve() == new_path.resolve():
            continue

        # Prevent overwriting existing files
        if new_path.exists():
            logger.error(f"Cannot rename '{file_info.path.name}' -> '{new_path.name}': Target already exists.")
            fail_count += 1
            continue

        try:
            os.rename(str(file_info.path), str(new_path))

            op = FileMoveOperation(
                original_path=str(file_info.path.resolve()),
                new_path=str(new_path.resolve()),
                timestamp=datetime.now().isoformat()
            )
            transaction.operations.append(op)
            success_count += 1
            logger.debug(f"Renamed: {file_info.path} -> {new_path}")

        except (OSError, PermissionError) as e:
            logger.error(f"Failed renaming '{file_info.path}' to '{new_path}': {e}")
            fail_count += 1

    if transaction.operations:
        save_transaction(transaction)

    logger.info(f"Batch rename complete. Success: {success_count}, Failed: {fail_count}")
    return transaction, success_count, fail_count
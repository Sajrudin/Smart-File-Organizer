import shutil
from datetime import datetime
from pathlib import Path

from history import save_transaction
from logger import setup_logger
from models import FileInfo, FileMoveOperation, Transaction

logger = setup_logger("organizer")


def resolve_collision(destination: Path) -> Path:
    """
    If destination file already exists, appends a timestamp
    suffix to prevent overwriting existing files.
    """
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]
    new_name = f"{stem}_{timestamp}{suffix}"
    return destination.parent / new_name


def organize_files(target_dir: Path, files: list[FileInfo]) -> tuple[Transaction, int, int]:
    """
    Organizes files into categorized subfolders under target_dir.
    Returns (transaction, successful_count, failed_count).
    """
    timestamp_str = datetime.now().isoformat()
    tx_id = f"tx_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    transaction = Transaction(
        transaction_id=tx_id,
        action_type="ORGANIZE",
        timestamp=timestamp_str,
        operations=[]
    )

    success_count = 0
    fail_count = 0

    for file_info in files:
        # Don't move files that are already inside a categorized folder in target_dir
        category_folder = target_dir / file_info.category
        category_folder.mkdir(parents=True, exist_ok=True)

        destination_path = category_folder / file_info.name

        # Skip if the file is already at its final destination
        if file_info.path.resolve() == destination_path.resolve():
            continue

        # Resolve potential name collisions
        final_destination = resolve_collision(destination_path)

        try:
            shutil.move(str(file_info.path), str(final_destination))
            
            # Record the successful operation
            op = FileMoveOperation(
                original_path=str(file_info.path.resolve()),
                new_path=str(final_destination.resolve()),
                timestamp=datetime.now().isoformat()
            )
            transaction.operations.append(op)
            success_count += 1
            logger.debug(f"Moved: {file_info.path} -> {final_destination}")

        except (OSError, PermissionError) as e:
            logger.error(f"Failed to move '{file_info.path}' to '{final_destination}': {e}")
            fail_count += 1

    # Save transaction only if operations were performed
    if transaction.operations:
        save_transaction(transaction)

    logger.info(
        f"Organization completed. Success: {success_count}, Failed: {fail_count}"
    )
    return transaction, success_count, fail_count
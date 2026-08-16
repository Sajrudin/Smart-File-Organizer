import json
import shutil
from dataclasses import asdict
from pathlib import Path
from config import HISTORY_DIR
from logger import setup_logger
from models import FileMoveOperation, Transaction

logger = setup_logger("history")


def save_transaction(transaction: Transaction) -> Path:
    """Saves a Transaction object to history/history_<id>.json."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    file_path = HISTORY_DIR / f"history_{transaction.transaction_id}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(asdict(transaction), f, indent=2)

    logger.info(f"Transaction {transaction.transaction_id} saved to {file_path}")
    return file_path


def load_latest_transaction() -> tuple[Transaction | None, Path | None]:
    """Finds and loads the most recent transaction log file."""
    if not HISTORY_DIR.exists():
        return None, None

    history_files = sorted(HISTORY_DIR.glob("history_*.json"))
    if not history_files:
        return None, None

    latest_file = history_files[-1]
    try:
        with open(latest_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        operations = [
            FileMoveOperation(
                original_path=op["original_path"],
                new_path=op["new_path"],
                timestamp=op["timestamp"]
            )
            for op in data.get("operations", [])
        ]

        transaction = Transaction(
            transaction_id=data["transaction_id"],
            action_type=data["action_type"],
            timestamp=data["timestamp"],
            operations=operations
        )
        return transaction, latest_file
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Failed to read transaction log '{latest_file}': {e}")
        return None, None


def rollback_transaction(transaction: Transaction, log_path: Path) -> tuple[int, int]:
    """
    Reverses all file move operations in reverse order.
    Returns a tuple of (successful_moves, failed_moves).
    """
    success_count = 0
    fail_count = 0

    logger.info(f"Starting rollback for transaction: {transaction.transaction_id}")

    # Process operations in reverse order
    for op in reversed(transaction.operations):
        current_path = Path(op.new_path)
        original_path = Path(op.original_path)

        if not current_path.exists():
            logger.warning(f"Cannot restore: file not found at '{current_path}'")
            fail_count += 1
            continue

        try:
            original_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(current_path), str(original_path))
            success_count += 1
            logger.debug(f"Restored: {current_path} -> {original_path}")
        except (OSError, PermissionError) as e:
            logger.error(f"Failed to move '{current_path}' back to '{original_path}': {e}")
            fail_count += 1

    # Remove the log file if rollback was completed
    if log_path.exists():
        log_path.unlink()
        logger.info(f"Removed transaction log file: {log_path}")

    return success_count, fail_count
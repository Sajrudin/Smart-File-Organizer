import hashlib
import os
from collections import defaultdict
from pathlib import Path

from config import HASH_CHUNK_SIZE
from logger import setup_logger
from models import FileInfo

logger = setup_logger("duplicates")


def calculate_sha256(file_path: Path, chunk_size: int = HASH_CHUNK_SIZE) -> str | None:
    """
    Computes the SHA256 hash of a file by streaming content in chunks.
    Avoids high memory usage on large files.
    """
    sha256_hash = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except (OSError, PermissionError) as e:
        logger.warning(f"Could not hash file '{file_path}': {e}")
        return None


def find_duplicates(files: list[FileInfo]) -> dict[str, list[FileInfo]]:
    """
    Finds duplicate files using a two-pass approach:
    1. Group files by exact byte size.
    2. Compute SHA256 hashes only for files with matching sizes.
    Returns a dictionary mapping sha256 hashes to lists of duplicate FileInfo objects.
    """
    # Pass 1: Group by size
    size_groups: dict[int, list[FileInfo]] = defaultdict(list)
    for file in files:
        if file.size_bytes > 0:  # Skip 0-byte empty files
            size_groups[file.size_bytes].append(file)

    # Filter out unique file sizes
    candidate_groups = [group for group in size_groups.values() if len(group) > 1]

    # Pass 2: Hash candidate files
    hash_groups: dict[str, list[FileInfo]] = defaultdict(list)

    for group in candidate_groups:
        for file in group:
            if not file.sha256:
                file.sha256 = calculate_sha256(file.path)

            if file.sha256:
                hash_groups[file.sha256].append(file)

    # Keep only groups with 2 or more files with matching content hashes
    duplicates = {
        h: file_list for h, file_list in hash_groups.items() if len(file_list) > 1
    }

    logger.info(f"Duplicate scan complete. Found {len(duplicates)} duplicate sets.")
    return duplicates


def delete_file(file_path: Path) -> bool:
    """Safely removes a file from disk."""
    try:
        os.remove(file_path)
        logger.info(f"Deleted duplicate file: {file_path}")
        return True
    except (OSError, PermissionError) as e:
        logger.error(f"Failed to delete file '{file_path}': {e}")
        return False
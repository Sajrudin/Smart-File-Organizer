import os
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from config import DEFAULT_CATEGORIES, IGNORED_DIRS, UNKNOWN_CATEGORY
from logger import setup_logger
from models import FileInfo, ScanResult

logger = setup_logger("scanner")


def get_file_category(extension: str) -> str:
    """Map a normalized file extension to its configured category."""
    ext_lower = extension.lower()
    for category, extensions in DEFAULT_CATEGORIES.items():
        if ext_lower in extensions:
            return category
    return UNKNOWN_CATEGORY


def scan_directory(target_path: Path) -> ScanResult:
    """
    Recursively scans the target directory, gathers file metadata,
    and returns a structured ScanResult object.
    """
    start_time = time.perf_counter()
    logger.info(f"Starting scan on directory: {target_path}")

    files: list[FileInfo] = []
    category_counts: dict[str, int] = defaultdict(int)
    total_size_bytes = 0

    for root, dirs, filenames in os.walk(target_path):
        # 1. Prune ignored directories in-place so os.walk does not traverse into them
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for filename in filenames:
            file_path = Path(root) / filename

            try:
                # 2. Extract file metadata safely
                stat_info = file_path.stat()
                size_bytes = stat_info.st_size
                modified_time = datetime.fromtimestamp(stat_info.st_mtime)
                extension = file_path.suffix.lower()
                category = get_file_category(extension)

                file_info = FileInfo(
                    name=filename,
                    path=file_path.resolve(),
                    size_bytes=size_bytes,
                    modified_time=modified_time,
                    category=category
                )

                files.append(file_info)
                category_counts[category] += 1
                total_size_bytes += size_bytes

            except (PermissionError, FileNotFoundError, OSError) as error:
                # 3. Log warning and continue scanning remaining files
                logger.warning(f"Could not access file '{file_path}': {error}")
                continue

    duration = time.perf_counter() - start_time
    logger.info(
        f"Scan complete: {len(files)} files found ({total_size_bytes} bytes) in {duration:.2f}s"
    )

    return ScanResult(
        root_path=target_path.resolve(),
        total_files=len(files),
        total_size_bytes=total_size_bytes,
        files=files,
        category_counts=dict(category_counts),
        scan_duration_seconds=duration
    )
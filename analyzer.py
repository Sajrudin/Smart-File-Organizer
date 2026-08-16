from collections import defaultdict
from models import FileInfo, ScanResult


def get_category_sizes(files: list[FileInfo]) -> dict[str, int]:
    """Calculate total size in bytes for each file category."""
    category_sizes: dict[str, int] = defaultdict(int)
    for file in files:
        category_sizes[file.category] += file.size_bytes
    return dict(category_sizes)


def get_category_percentages(category_sizes: dict[str, int], total_size_bytes: int) -> dict[str, float]:
    """Calculate the percentage of total storage consumed by each category."""
    if total_size_bytes == 0:
        return {cat: 0.0 for cat in category_sizes}

    return {
        cat: (size / total_size_bytes) * 100.0
        for cat, size in category_sizes.items()
    }


def get_largest_files(files: list[FileInfo], limit: int = 10) -> list[FileInfo]:
    """Return the top N largest files sorted by size in descending order."""
    return sorted(files, key=lambda f: f.size_bytes, reverse=True)[:limit]


def analyze_storage(scan_result: ScanResult, top_n: int = 10) -> dict:
    """
    Perform complete storage analytics on a ScanResult object.
    Returns a dictionary of aggregated metrics.
    """
    category_sizes = get_category_sizes(scan_result.files)
    category_percentages = get_category_percentages(
        category_sizes, scan_result.total_size_bytes
    )
    largest_files = get_largest_files(scan_result.files, limit=top_n)

    return {
        "root_path": scan_result.root_path,
        "total_files": scan_result.total_files,
        "total_size_bytes": scan_result.total_size_bytes,
        "category_counts": scan_result.category_counts,
        "category_sizes": category_sizes,
        "category_percentages": category_percentages,
        "largest_files": largest_files,
        "scan_duration_seconds": scan_result.scan_duration_seconds,
    }
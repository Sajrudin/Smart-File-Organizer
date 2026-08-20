import json
from datetime import datetime
from pathlib import Path

from config import REPORTS_DIR
from logger import setup_logger
from models import ScanResult
from utils import format_size

logger = setup_logger("reporter")


def generate_text_report(scan_result: ScanResult, analysis_data: dict) -> Path:
    """
    Generates a structured, human-readable text report summarizing
    storage distribution and the largest files found.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = REPORTS_DIR / f"report_{timestamp}.txt"

    lines = [
        "=" * 60,
        "SMART FILE ORGANIZER & STORAGE REPORT",
        f"Generated At : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Target Path  : {scan_result.root_path}",
        "=" * 60,
        "",
        "OVERVIEW:",
        f"  Total Files Found   : {scan_result.total_files:,}",
        f"  Total Storage Used  : {format_size(scan_result.total_size_bytes)}",
        f"  Scan Duration       : {scan_result.scan_duration_seconds:.2f} seconds",
        "",
        "-" * 60,
        "STORAGE DISTRIBUTION BY CATEGORY:",
        f"{'Category':<15} {'Files':<10} {'Size':<15} {'Percentage'}",
        "-" * 60,
    ]

    category_sizes = analysis_data.get("category_sizes", {})
    category_percentages = analysis_data.get("category_percentages", {})

    for category, count in scan_result.category_counts.items():
        size_str = format_size(category_sizes.get(category, 0))
        pct_str = f"{category_percentages.get(category, 0.0):.2f}%"
        lines.append(f"{category:<15} {count:<10} {size_str:<15} {pct_str}")

    lines.extend([
        "",
        "-" * 60,
        "TOP LARGEST FILES:",
        "-" * 60,
    ])

    largest_files = analysis_data.get("largest_files", [])
    for idx, file_info in enumerate(largest_files, 1):
        lines.append(
            f"  {idx:2d}. {file_info.name} ({format_size(file_info.size_bytes)}) - {file_info.path}"
        )

    lines.append("\n" + "=" * 60 + "\n")

    report_content = "\n".join(lines)
    file_path.write_text(report_content, encoding="utf-8")
    logger.info(f"Text report generated at: {file_path}")

    return file_path


def generate_json_report(scan_result: ScanResult, analysis_data: dict) -> Path:
    """
    Generates a machine-readable JSON report containing full
    scan metadata and calculated storage distributions.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = REPORTS_DIR / f"report_{timestamp}.json"

    data = {
        "generated_at": datetime.now().isoformat(),
        "root_path": str(scan_result.root_path),
        "total_files": scan_result.total_files,
        "total_size_bytes": scan_result.total_size_bytes,
        "total_size_formatted": format_size(scan_result.total_size_bytes),
        "scan_duration_seconds": scan_result.scan_duration_seconds,
        "category_counts": scan_result.category_counts,
        "category_sizes": analysis_data.get("category_sizes", {}),
        "category_percentages": analysis_data.get("category_percentages", {}),
        "largest_files": [
            {
                "name": f.name,
                "path": str(f.path),
                "size_bytes": f.size_bytes,
                "size_formatted": format_size(f.size_bytes),
                "category": f.category,
            }
            for f in analysis_data.get("largest_files", [])
        ],
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    logger.info(f"JSON report generated at: {file_path}")
    return file_path
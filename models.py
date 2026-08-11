from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
import os


@dataclass
class FileInfo:
    """
    Represents a file with its metadata.

    Attributes:
        name: Name of the file (e.g., "report.pdf").
        path: The full path to the file on the filesystem.
        size_bytes: Size of the file in bytes.
        modified_time: Last modification time of the file.
        category: The category this file belongs to (e.g., "Documents", "Images").
        sha256: The SHA256 hash of the file content, used for identifying duplicates. Optional.
    """

    name: str
    path: Path
    size_bytes: int
    modified_time: datetime
    category: str
    sha256: str | None = None


@dataclass
class ScanResult:
    """
    Represents the result of a filesystem scan.

    Attributes :
        root_path : Path = The directory in which the scan is done.
        total_files : int - Total number of files found.
        total_size_bytes : int - Total size of files found in bytes.
        files : List[FileInfo] - List of the files(FileInfo object) found.
        category_count: Dict[str, int] - Count of each type of files found like image, docs etc.
        scan_duration: float - Time taken to scan the directory.
    """

    root_path: Path
    total_files: int
    total_size_bytes: int
    files: list[FileInfo]
    category_counts: dict[str, int]
    scan_duration_seconds: float
    


if __name__ == "__main__":
    file = FileInfo(
        "Sample.txt",
        Path(os.path.join(os.getcwd(), "Sample.txt")),
        2048,
        datetime.now(),
        "Text",
        "54321"
    )

    scan_result = ScanResult(
        Path.cwd(),
        1,
        2048,
        [file],
        {'text' : 1},
        0.2
    )
    print(scan_result)
    
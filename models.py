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


if __name__ == "__main__":
    file = FileInfo(
        "Sample.txt",
        Path(os.getcwd()),
        2048,
        datetime.now(),
        "Text",
        "54321"
    )

    print(file)
    
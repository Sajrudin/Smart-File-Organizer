from pathlib import Path   

def format_size(size_bytes : int) -> str:
    """Convert bytes into human-readable string units (B, KB, MB, GB, TB)."""
    if size_bytes < 0:
        raise ValueError(f'File size cannot negative')
    
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_index = 0

    size = float(size_bytes)

    while size >= 1024 and unit_index < len(units) - 1:

        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"


def validate_path(path_str: str) -> Path:
    """
    Validate that a given string path exists and is a directory.
    Returns the resolved Path object.
    """
    path = Path(path_str).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")

    return path
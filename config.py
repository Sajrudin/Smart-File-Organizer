from pathlib import Path

# Base Paths
ROOT_DIR = Path(__file__).parent.resolve()
REPORTS_DIR = ROOT_DIR / "reports"
HISTORY_DIR = ROOT_DIR / "history"
LOGS_DIR = ROOT_DIR / "logs"


# File Hashing Configuration
HASH_CHUNK_SIZE = 65536  # 64KiB chunk size for hashing files    

# Ignored Directories (Skipped during recursive scanning)
IGNORED_DIRS = {
    ".git", ".svn", "__pycache__", ".venv", "node_modules",
    "$RECYCLE.BIN", "System Volume Information"
}

# Category Extension Mappings
DEFAULT_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".md"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
    "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json"],
    "Executables": [".exe", ".msi", ".bat", ".sh"]
}

# Default Category for unrecognized extensions
UNKNOWN_CATEGORY = "Others"
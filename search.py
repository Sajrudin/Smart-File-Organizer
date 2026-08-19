import fnmatch
import re
from logger import setup_logger
from models import FileInfo

logger = setup_logger("search")


def search_by_substring(files: list[FileInfo], query: str) -> list[FileInfo]:
    """Case-insensitive substring match on filename."""
    query_lower = query.lower()
    return [f for f in files if query_lower in f.name.lower()]


def search_by_glob(files: list[FileInfo], pattern: str) -> list[FileInfo]:
    """Unix shell-style wildcard matching (e.g., '*.pdf', 'IMG_202?.*')."""
    return [f for f in files if fnmatch.fnmatch(f.name.lower(), pattern.lower())]


def search_by_regex(files: list[FileInfo], regex_pattern: str) -> list[FileInfo]:
    """Regex pattern search across filenames with syntax validation."""
    try:
        compiled_regex = re.compile(regex_pattern, re.IGNORECASE)
    except re.error as e:
        logger.error(f"Invalid regex pattern '{regex_pattern}': {e}")
        return []

    return [f for f in files if compiled_regex.search(f.name)]


def search_files(
    files: list[FileInfo],
    query: str,
    search_type: str = "substring",
    category_filter: str | None = None,
) -> list[FileInfo]:
    """
    Search orchestrator across a list of FileInfo objects.
    search_type can be: 'substring', 'glob', or 'regex'.
    """
    if category_filter:
        files = [f for f in files if f.category.lower() == category_filter.lower()]

    if search_type == "glob":
        results = search_by_glob(files, query)
    elif search_type == "regex":
        results = search_by_regex(files, query)
    else:
        results = search_by_substring(files, query)

    logger.info(
        f"Search query='{query}' (type={search_type}) found {len(results)} matches."
    )
    return results
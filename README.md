# 🗂️ Smart File Organizer

A modular Python CLI application for **organizing files, analyzing storage usage, finding duplicates, searching files, batch renaming, generating reports, and rolling back supported file operations**.

Built as a practical Python software-engineering project with a focus on clean architecture, reusable services, safe file operations, logging, and automated testing.

> The complete implementation process and development details are documented separately in [`implementationplan.md`](implementationplan.md).

## 📌 Features

- **⚡ Recursive Directory Scanner**: Fast recursive directory traversal using in-place directory pruning (`dirs[:]`) to skip system folders and dependency caches (`.git`, `node_modules`, `__pycache__`)[cite: 1].
- **📊 Storage Analytics**: Real-time storage consumption breakdown by file category with percentage distribution and Top-$N$ largest files identification[cite: 1].
- **🧹 Transactional File Organizer**: Sorts messy folders into clean categorical directories with automatic timestamp-based collision handling (`filename_YYYYMMDD_HHMMSS.ext`)[cite: 1].
- **🔍 Two-Pass SHA-256 Deduplication**: Zero-I/O size grouping followed by constant-memory 64 KiB chunked hashing to detect exact content duplicates safely[cite: 1].
- **🔎 Multi-Mode Search Engine**: Filter files using substring matches, shell wildcard globs (`fnmatch`), or regular expressions (`re`) combined with category filters[cite: 1].
- **🏷️ Batch File Renamer**: Preview batch renaming plans with sequential zero-padding patterns (e.g., `Archive_###`) before applying changes[cite: 1].
- **⏪ Atomic Undo / Rollback**: Records every disk mutation into structured JSON transaction logs and restores files in exact reverse order[cite: 1].
- **📑 Dual Reporting**: Generates human-readable (`.txt`) and machine-readable (`.json`) storage reports[cite: 1].
- **🛡️ Production Logging**: Dual-handler logging via `RotatingFileHandler` (capturing `DEBUG` logs to disk while outputting clean `WARNING`/`ERROR` messages to the console)[cite: 1].

## 🧱 Project Architecture

The application follows a **monolithic layered architecture** with separation of concerns:

```text
CLI
 │
 ▼
Application Operations
 │
 ▼
Service Modules
 │
 ├── Scanner
 ├── Analyzer
 ├── Organizer
 ├── Duplicates
 ├── Search
 ├── Renamer
 ├── Reporter
 └── History
 │
 ▼
Models / Utilities / Configuration / Logger
```

This keeps user interaction, application orchestration, business logic, and supporting components separated.

## Algorithms & Techniques

A few notable techniques used in the project:

- **Recursive filesystem traversal** using `os.walk()`
- **Two-pass duplicate detection**
  - Group files by exact size
  - Calculate SHA-256 only for matching-size candidates
- **Chunk-based file hashing** to avoid loading large files completely into memory
- **Glob and regular-expression pattern matching**
- **Collision resolution** using timestamp-based filenames
- **Dry-run planning** before batch rename execution
- **Transaction logging and reverse-order rollback**
- **Structured JSON serialization** for future integrations and dashboards

### Complexity Highlights

| Operation | Complexity |
|---|---:|
| Directory scanning | O(F + D) |
| Storage aggregation | O(F) |
| Largest-file sorting | O(F log F) |
| Duplicate size grouping | O(F) |
| SHA-256 hashing | O(B) |
| Batch rename planning | O(F) |
| Rollback | O(O) |

Where:

- `F` = number of files
- `D` = number of directories
- `B` = total bytes read during hashing
- `O` = number of recorded operations

## Project Structure

```text
Smart-File-Organizer/
│
├── main.py
├── operations.py
├── scanner.py
├── analyzer.py
├── organizer.py
├── duplicates.py
├── search.py
├── renamer.py
├── history.py
├── report.py
│
├── models.py
├── config.py
├── logger.py
├── utils.py
│
├── tests/
├── implementationplan.md
├── requirements.txt
└── .gitignore
```

Generated runtime data such as reports, history, logs, and local sample data is excluded from Git.

## Installation

```bash
git clone <your-repository-url>
cd Smart-File-Organizer

## Use python version greater than 3.10
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The application provides an interactive menu for all major operations.

For manual testing, use a disposable `sample_data/` directory containing different file types, sizes, nested folders, and duplicate files.

## Testing

Run the complete test suite with:

```bash
pytest -v
```

Current test result:

```text
22 passed
100% success rate
```

The tests cover scanning, analysis, duplicate detection, organization, collision handling, rename operations, rollback, searching, and utility functions.

## Reports & Future Integration

The application can generate both **TXT and JSON reports**.

The JSON output provides structured storage information that can later be consumed by a dashboard or API without changing the core file-processing services.

```text
File Organizer
      │
      ▼
   Analysis
      │
      ▼
   JSON Report
      │
      ├── Dashboard
      ├── API
      └── Data Visualization
```

## Technical Highlights

**Python • OOP • Layered Architecture • Dataclasses • pathlib • File System Operations • SHA-256 • Regex • JSON • Logging • Transactions • Rollback • Pytest**

## Future Scope

- Web-based storage dashboard
- REST API integration
- Safer recycle-bin based deletion
- Database-backed history
- Scheduled storage analysis
- Additional file organization rules

## License

This project is intended for learning, experimentation, and portfolio use.

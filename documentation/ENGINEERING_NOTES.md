# Engineering Concepts

# PHASE 1

## Concept 1: What is the architecture of our application?

The architecture of the application is a monolithic layered architecture. It means separating the each functionality into different modules/layers for maintainability, scalability, and reusability.

### Monolithic Architecture

A monolithic architecture is a software design pattern in which all the components of an application are tightly coupled and run as a single process. It is a traditional approach to software development and is well-suited for small to medium-sized applications. It is also easy to deploy as it involves deploying a single artifact.

### Layered Architecture

A layered architecture is a software design pattern in which the components of an application are organized into layers, each with a specific responsibility. The layers are organized in a hierarchical manner, with each layer having access to the layers below it.

---

## Concept 2 : Separation of Concern

This refers to each module having its own concern(functionality). In other words , it means dividing the application into different modules based on the functionality they provide.

A concern simply means a particular responsibility or job that the software needs to handle.

For my project :

* Scanning files       → one concern
* Analyzing storage    → another concern
* Moving files         → another concern
* Finding duplicates   → another concern
* Generating reports   → another concern
* User interaction     → another concern

---

## Concept 3: Layered Architecture

Now that you understand separation of concerns, we can introduce one additional idea: how those separate responsibilities are organized and allowed to interact.

My implementation plan is to implement this application using Layered Architecture.

Think of it as arranging our modules into levels.

### Q. What does "layer" mean?

**A.** A layer is basically a level of responsibility.

For example, the top layer is concerned with:

1. "What does the user want?"

The service layer is concerned with:

2. "How do I perform that operation?"

And the filesystem is concerned with:

3. "How do I actually read/write/move files?"

---

## Concept 4: What is a Data Model?

A defined structure that represents an entity in an application by specifying the information it contains and how that information is organized. In this project, FileInfo provides a standardized representation of a file, allowing different services to work with consistent file data instead of relying on loosely structured dictionaries.

```python
    file_info = {
    "path": "...",
    "name": "resume.pdf",
    "extension": ".pdf",
    "size_bytes": 245000,
    "category": "Documents",
    "modified_time": "...",
    "sha256": None }
```

---

## Concept 5: Why dataclass for FileInfo?

We're using a dataclass because FileInfo is primarily a structured data object, and dataclasses let us define that structure clearly while automatically handling common object boilerplate.

---

## Concept 6: Why use Path instead of a string for file paths?

In our system, we are using :

* path : Path

instead of :

* path : str

As it helps by providing various function for manipulation and accessing file path.

> Path provides a filesystem-aware abstraction for paths, giving us methods and properties for working with files and directories while reducing manual string manipulation.

---

## Concept 9: Why do we need ScanResult?

FileInfo represents an individual file, while ScanResult represents the overall outcome and metadata of a scanning operation.

So we have a hierarchy:

```text
                 ScanResult
                     │
       ┌─────────────┼─────────────┐
       │             │             │
   root_path    total_files     total_size
       │
       │
       └────── files ──────────────┐
                                   │
                         ┌─────────┴─────────┐
                         ▼         ▼         ▼
                      FileInfo  FileInfo  FileInfo
```

In other words, FileInfo represents one individual file, while ScanResult represents the complete outcome of a scanning operation, including the collection of discovered FileInfo objects and aggregate information such as total files, total size, categories, and scan duration. This allows other services to reuse the scan result instead of repeatedly scanning the filesystem.

### The important relationship :

```text
    Scanner
      │
      │ scans filesystem
      ▼
   ScanResult
      │
      ├── FileInfo
      ├── FileInfo
      ├── FileInfo
      ├── ...
      │
      ├── total_files
      ├── total_size_bytes
      ├── category_counts
      └── scan_duration
```

---

## Concept 10: Why use loggers?

Logging is a way to record events that happen while a program is running. Our logger is set up to send these messages to both a file (detailed, permanent storage) and the console (real-time feedback for the user). It allows us to track what the application is doing, diagnose problems, and understand usage patterns without disrupting the application's normal operation.

The logging is divided into 2 parts :

* FileHandler
* Console_Handler

### The Logging flowchart is :

```text
┌──────────────────────────────────────────────────────────────────────┐
│                        SMART FILE ORGANIZER                           │
└──────────────────────────────────────────────────────────────────────┘
                                     │
                             ┌─────────────────┐
                             │  SETUP LOGGER   │
                             │  (setup_logger) │
                             └────────┬────────┘
                                      │
                        ┌─────────────┼─────────────┐
                        ▼             ▼             ▼
                LOGS_DIR exists?   Create if NOT   Set Level: DEBUG
                        │             │             │
                        └─────────────┼─────────────┘
                                      │
                              ┌──────────────────┐
                              │  Console Handler │
                              │  Level: WARNING  │
                              └────────┬─────────┘
                                       │
                              ┌──────────────────┐
                              │   File Handler   │
                              │  Level: DEBUG    │
                              └────────┬─────────┘
                                       │
                      Returns Logger Object (DEBUG+) │
                                       │
                        ┌────────────────────────────────┐
                        │        LOGGING OUTPUT            │
                        ├────────────────────────────────┤
                        │ DEBUG → File Only              │
                        │ INFO  → File Only              │
                        │ WARNING → Console & File       │
                        │ ERROR → Console & File       │
                        └────────────────────────────────┘
```

### Q. Why two handlers?

1. Console Handler: We only want to see "important" messages in the terminal (warnings and errors). We don't want the terminal flooded with "Scanning file X..." messages.
2. File Handler: We want to record EVERYTHING for later review. If something goes wrong, we want the full DEBUG-level log.

### Q. Why different log levels?

* DEBUG: Very detailed. Used for tracing code execution.
* INFO: General information about program flow.
* WARNING: Something unexpected but not critical happened.
* ERROR: A critical error occurred that stopped some functionality.

# PHASE 1 ( COMPLETED )

## Concept 11: Serialization

* Converting Python object to Json/Dictionary is called as Serialization
* using asdict() and json.dump() for writing to file

---

## Concept 12: Deserialization

* Converting JSON to Python object is called as Deserialization
* using json.load()

---

## Concept 13: Transaction

* One logical operation containing multiple smaller operations is called a transaction

```text
Transaction
   ├── Operation
   ├── Operation
   └── Operation
```

---

## Concept 14: RollBack

* Undoing a transaction.

```text
      A -> B
    becomes
      B -> A
```

---

## Concept 15 : Transactional File Organization & Undo Engine

* **Two-Layer Data Modeling for Rollback Safety**:

  * `FileMoveOperation`: Records atomic path transitions (`original_path` $\rightarrow$ `new_path`) alongside a timestamp.
  * `Transaction`: Encapsulates a batch of operations under a single `transaction_id` and `action_type` (e.g., `"ORGANIZE"`, `"RENAME"`).

* **Log-Before-Mutate Principle**:

  * Every planned disk move is staged into an in-memory transaction before or immediately upon executing `shutil.move()`.
  * Completed transactions persist to disk as `history/history_<tx_id>.json` to ensure recovery across application restarts.

* **Collision Prevention (`resolve_collision`)**:

  * Moving files from multi-level directory structures into flattened category folders creates name collisions (e.g., multiple `notes.txt` files).
  * Automatic collision handling appends timestamp tokens (`filename_YYYYMMDD_HHMMSS.ext`) to avoid data overwrites.

* **Reverse-Order Rollback Strategy**:

  * Transactions must roll back in exact reverse chronological order (`reversed(tx.operations)`).
  * Parent directory creation (`mkdir(parents=True, exist_ok=True)`) is enforced prior to file restoration to handle cases where source folders were pruned.

---

## Concept 16 : Chunked SHA-256 Duplicate Detection Engine

* **Two-Pass I/O Optimization Filter**:

  * **Pass 1 (Zero-I/O Size Binning)**: Files are grouped strictly by `size_bytes` using in-memory metadata. Files with unique sizes are skipped, eliminating up to 90%+ of disk read operations.
  * **Pass 2 (Targeted Hashing)**: SHA-256 hashing is executed only on size-collision candidate pools ($N \ge 2$).

* **Constant-Memory Hashing (`HASH_CHUNK_SIZE = 65536`)**:

  * Direct `.read()` loads entire files into RAM, causing `OutOfMemoryError` on multi-gigabyte media.
  * Streaming disk reads in fixed 64 KiB chunks through `hashlib.sha256().update()` keeps RAM utilization constant ($O(1)$) regardless of file size.

* **Lazy Hash Evaluation & Safe Deletion**:

  * The `FileInfo.sha256` attribute is populated lazily only when duplicate analysis is explicitly invoked.
  * Confirmed duplicates require explicit identifier groupings ($H(f_1) = H(f_2)$) before presenting selective removal via `os.remove()`.

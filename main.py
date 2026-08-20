import sys
from models import ScanResult
from operations import (
    run_scan,
    run_analysis,
    run_organize,
    run_duplicate_detection,
    run_delete_duplicate,
    run_search,
    run_rename_preview,
    run_rename_execute,
    run_generate_reports,
    run_undo,
)
from utils import format_size


def display_menu() -> None:
    """Displays the primary CLI menu."""
    print("\n" + "=" * 50)
    print("      SMART FILE ORGANIZER & STORAGE ANALYZER")
    print("=" * 50)
    print(" [1] Scan Directory")
    print(" [2] View Storage Analytics & Top Files")
    print(" [3] Organize Files by Category")
    print(" [4] Find & Manage Duplicate Files")
    print(" [5] Search Files (Substring / Wildcard / Regex)")
    print(" [6] Batch Rename Files (with Dry-Run Preview)")
    print(" [7] Generate TXT & JSON Reports")
    print(" [8] Undo Last Operation (Rollback)")
    print(" [0] Exit")
    print("-" * 50)


def prompt_path() -> str:
    """Prompts for target directory."""
    return input("Enter target directory path: ").strip()


def handle_scan(current_scan: ScanResult | None) -> ScanResult | None:
    path_str = prompt_path()
    try:
        scan_result = run_scan(path_str)
        print(f"\nScan completed successfully in {scan_result.scan_duration_seconds:.2f}s!")
        print(f"Total Files Found: {scan_result.total_files:,}")
        print(f"Total Storage Used: {format_size(scan_result.total_size_bytes)}")
        return scan_result
    except Exception as e:
        print(f"\nError during scan: {e}")
        return current_scan


def handle_analysis(scan_result: ScanResult | None) -> None:
    if not scan_result:
        print("\nPlease run a scan first (Option 1).")
        return

    analysis = run_analysis(scan_result)
    print(f"\n--- Storage Analytics for: {analysis['root_path']} ---")
    print(f"{'Category':<15} {'Files':<10} {'Size':<15} {'Percentage'}")
    print("-" * 50)
    for cat, count in scan_result.category_counts.items():
        size_str = format_size(analysis['category_sizes'].get(cat, 0))
        pct_str = f"{analysis['category_percentages'].get(cat, 0.0):.2f}%"
        print(f"{cat:<15} {count:<10} {size_str:<15} {pct_str}")

    print("\n--- Top Largest Files ---")
    for idx, f in enumerate(analysis["largest_files"], 1):
        print(f" {idx:2d}. {f.name} ({format_size(f.size_bytes)}) - {f.path}")


def handle_organize(scan_result: ScanResult | None) -> ScanResult | None:
    path_str = prompt_path()
    confirm = input("Are you sure you want to organize files into subfolders? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Organization cancelled.")
        return scan_result

    try:
        result = run_organize(path_str, scan_result)
        print(f"\nOrganization complete!")
        print(f"Transaction ID   : {result['transaction_id']}")
        print(f"Successful Moves : {result['successful_moves']}")
        print(f"Failed Moves     : {result['failed_moves']}")
        return None  # Invalidate cached scan since files have moved
    except Exception as e:
        print(f"\nError during organization: {e}")
        return scan_result


def handle_duplicates(scan_result: ScanResult | None) -> None:
    if not scan_result:
        print("\nPlease run a scan first (Option 1).")
        return

    print("\nScanning for duplicate files (SHA-256)...")
    duplicates = run_duplicate_detection(scan_result)
    if not duplicates:
        print("No duplicate files found!")
        return

    print(f"\nFound {len(duplicates)} sets of duplicate files:")
    for hash_val, file_list in duplicates.items():
        print(f"\n[Hash: {hash_val[:12]}...] ({format_size(file_list[0].size_bytes)} each)")
        for idx, f in enumerate(file_list, 1):
            print(f"  [{idx}] {f.path}")
        
        del_choice = input("Enter file numbers to delete (e.g., '2,3') or press Enter to keep all: ").strip()
        if del_choice:
            for item in del_choice.split(","):
                try:
                    file_idx = int(item.strip()) - 1
                    if 0 <= file_idx < len(file_list):
                        run_delete_duplicate(file_list[file_idx].path)
                        print(f"Deleted: {file_list[file_idx].name}")
                except ValueError:
                    continue


def handle_search(scan_result: ScanResult | None) -> None:
    if not scan_result:
        print("\nPlease run a scan first (Option 1).")
        return

    print("\nSearch Types: [1] Substring (default)  [2] Wildcard/Glob  [3] Regex")
    type_choice = input("Select search type (1-3): ").strip()
    type_map = {"1": "substring", "2": "glob", "3": "regex"}
    search_type = type_map.get(type_choice, "substring")

    query = input("Enter search query: ").strip()
    cat_filter = input("Enter category filter (or press Enter to skip): ").strip() or None

    matches = run_search(scan_result.files, query, search_type, cat_filter)
    print(f"\nFound {len(matches)} matching files:")
    for idx, f in enumerate(matches, 1):
        print(f"  {idx:2d}. {f.name} ({f.category}) - {f.path}")


def handle_rename(scan_result: ScanResult | None) -> ScanResult | None:
    if not scan_result:
        print("\nPlease run a scan first (Option 1).")
        return

    pattern = input("Enter renaming pattern (e.g., 'Photo_###'): ").strip()
    if not pattern:
        print("Pattern cannot be empty.")
        return scan_result

    plan = run_rename_preview(scan_result.files, pattern)
    print("\n--- Dry-Run Rename Preview ---")
    for file_info, new_path in plan[:15]:
        print(f"  {file_info.name} -> {new_path.name}")
    if len(plan) > 15:
        print(f"  ... and {len(plan) - 15} more files.")

    confirm = input("\nExecute this renaming plan? (y/n): ").strip().lower()
    if confirm == 'y':
        result = run_rename_execute(plan)
        print(f"\nBatch rename executed!")
        print(f"Transaction ID : {result['transaction_id']}")
        print(f"Renamed        : {result['successful_renames']}")
        print(f"Failed         : {result['failed_renames']}")
        return None  # Invalidate cached scan
    else:
        print("Rename operation cancelled.")
        return scan_result


def handle_reports(scan_result: ScanResult | None) -> None:
    if not scan_result:
        print("\nPlease run a scan first (Option 1).")
        return

    analysis = run_analysis(scan_result)
    txt_path, json_path = run_generate_reports(scan_result, analysis)
    print(f"\nReports generated successfully:")
    print(f"  Text Report : {txt_path}")
    print(f"  JSON Report : {json_path}")


def handle_undo() -> None:
    confirm = input("Are you sure you want to rollback the last operation? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Rollback cancelled.")
        return

    result = run_undo()
    if result.get("status") == "no_history":
        print(f"\n{result['message']}")
    else:
        print(f"\nRollback completed successfully!")
        print(f"Transaction ID : {result['transaction_id']}")
        print(f"Action Type    : {result['action_type']}")
        print(f"Restored Files : {result['successful_restores']}")
        print(f"Failed Restores: {result['failed_restores']}")


def main() -> None:
    current_scan: ScanResult | None = None

    while True:
        display_menu()
        choice = input("Select an option (0-8): ").strip()

        if choice == "1":
            current_scan = handle_scan(current_scan)
        elif choice == "2":
            handle_analysis(current_scan)
        elif choice == "3":
            current_scan = handle_organize(current_scan)
        elif choice == "4":
            handle_duplicates(current_scan)
        elif choice == "5":
            handle_search(current_scan)
        elif choice == "6":
            current_scan = handle_rename(current_scan)
        elif choice == "7":
            handle_reports(current_scan)
        elif choice == "8":
            handle_undo()
            current_scan = None
        elif choice == "0":
            print("\nExiting Smart File Organizer. Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please select a number between 0 and 8.")


if __name__ == "__main__":
    main()
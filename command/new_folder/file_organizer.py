"""Console utility that sorts files into subfolders by extension."""

import argparse
import shutil
import sys
from pathlib import Path

EXTENSION_MAP: dict[str, str] = {
    # images
    ".jpg": "images", ".jpeg": "images", ".jfif": "images",
    ".png": "images", ".gif": "images", ".bmp": "images",
    ".tiff": "images", ".tif": "images", ".webp": "images",
    ".svg": "images", ".ico": "images", ".heic": "images",
    # documents
    ".pdf": "documents", ".doc": "documents", ".docx": "documents",
    ".xls": "documents", ".xlsx": "documents", ".ppt": "documents",
    ".pptx": "documents", ".odt": "documents", ".ods": "documents",
    ".odp": "documents", ".rtf": "documents", ".txt": "documents",
    ".csv": "documents", ".md": "documents", ".ipynb": "documents",
    # archives
    ".zip": "archives", ".tar": "archives", ".gz": "archives",
    ".bz2": "archives", ".xz": "archives", ".7z": "archives",
    ".rar": "archives", ".tgz": "archives",
    # video
    ".mp4": "video", ".avi": "video", ".mkv": "video",
    ".mov": "video", ".wmv": "video", ".flv": "video",
    ".webm": "video", ".m4v": "video",
    # audio
    ".mp3": "audio", ".wav": "audio", ".flac": "audio",
    ".aac": "audio", ".ogg": "audio", ".wma": "audio",
    ".m4a": "audio", ".opus": "audio",
    # code
    ".py": "code", ".js": "code", ".ts": "code",
    ".html": "code", ".css": "code", ".c": "code",
    ".cpp": "code", ".h": "code", ".java": "code",
    ".rs": "code", ".go": "code", ".rb": "code",
    ".sh": "code", ".bash": "code", ".sql": "code",
    ".json": "code", ".xml": "code", ".yaml": "code",
    ".yml": "code", ".toml": "code", ".ini": "code",
    ".cfg": "code", ".r": "code",
}


def get_category(suffix: str) -> str:
    """Return the category for a file suffix (lowercase), or 'other'."""
    return EXTENSION_MAP.get(suffix.lower(), "other")


def organize(folder: Path, *, dry_run: bool = False) -> dict[str, int]:
    """Sort files in *folder* into category subfolders.

    Args:
        folder: Path to the target directory.
        dry_run: If True, only print planned moves; do not touch the disk.

    Returns:
        Dict mapping category names to the number of files processed (moved or
        skipped) for that category.

    Raises:
        SystemExit: If *folder* does not exist or is not a directory.
    """
    folder = folder.resolve()

    if not folder.exists():
        sys.exit(f"Error: '{folder}' does not exist.")
    if not folder.is_dir():
        sys.exit(f"Error: '{folder}' is not a directory.")

    counts: dict[str, int] = {}

    for entry in sorted(folder.iterdir()):
        if not entry.is_file():
            continue

        suffix = entry.suffix
        category = get_category(suffix)

        target_dir = folder / category
        target_path = target_dir / entry.name

        if not dry_run:
            target_dir.mkdir(exist_ok=True)

        if target_path.exists():
            print(f"SKIP  {entry.name}  (already exists in {category}/)")
            counts[category] = counts.get(category, 0) + 1
            continue

        if dry_run:
            print(f"[DRY RUN] Move  {entry.name}  ->  {category}/")
        else:
            shutil.move(str(entry), str(target_path))
            print(f"MOVE  {entry.name}  ->  {category}/")

        counts[category] = counts.get(category, 0) + 1

    return counts


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sort files in a folder into category subfolders by extension."
    )
    parser.add_argument(
        "folder", type=Path,
        help="Path to the folder to organize."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print planned moves without making changes."
    )
    args = parser.parse_args()

    counts = organize(args.folder, dry_run=args.dry_run)

    if not counts:
        print("No files to organize.")
        return

    print()
    print("--- Summary ---")
    for cat in ["images", "documents", "archives", "video", "audio", "code", "other"]:
        if cat in counts:
            print(f"  {cat}: {counts[cat]}")


if __name__ == "__main__":
    main()

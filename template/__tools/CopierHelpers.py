import os
import shutil

from pathlib import Path
from typing import Optional


# ----------------------------------------------------------------------
def EnsureFile(
    path: Path,
) -> Path:
    if not path.is_file():
        raise ValueError(f"'{path}' is not a file.")

    return path


# ----------------------------------------------------------------------
def EnsureDir(
    path: Path,
) -> Path:
    if not path.is_dir():
        raise ValueError(f"'{path}' is not a directory.")

    return path


# ----------------------------------------------------------------------
def MoveFile(
    source_filename: Path,
    dest_dir: Path,
    dest_filename: Optional[str] = None,
) -> None:
    EnsureFile(source_filename)

    dest_fullpath = dest_dir / (dest_filename or source_filename.name)

    dest_fullpath.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(source_filename, dest_fullpath)


# ----------------------------------------------------------------------
def MoveFiles(
    source_dir: Path,
    dest_dir: Path,
) -> None:
    EnsureDir(source_dir)

    for root_str, _, filenames in os.walk(source_dir):
        if not filenames:
            continue

        root = Path(root_str)

        relative_path = root.relative_to(source_dir)

        (dest_dir / relative_path).mkdir(parents=True, exist_ok=True)

        for filename in filenames:
            if filename == "__postprocess.py":
                continue

            source_filename = root / filename
            dest_filename = dest_dir / relative_path / filename

            shutil.move(source_filename, dest_filename)


# ----------------------------------------------------------------------
def AugmentFile(
    filename: Path,
    tags: Optional[str],
    new_content: str,
) -> None:
    if not filename.is_file():
        filename.parent.mkdir(parents=True, exist_ok=True)
        content = ""
    else:
        with filename.open(encoding="utf-8") as f:
            content = f.read()

    if tags:
        raise Exception("Not implemented yet")
    else:
        content += new_content

    with filename.open("w", encoding="utf-8") as f:
        f.write(content)

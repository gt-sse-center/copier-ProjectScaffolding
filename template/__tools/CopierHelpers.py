import os
import re
import shutil

from pathlib import Path
from typing import Callable, Optional, Pattern


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
def ReplaceContent(
    file_extension: str,
    tag_name: str,
    content: str,
    new_content: str,
) -> str:
    regex_factory_func = next(
        (value for key, value in _regex_lookup.items() if file_extension in key),
        None,
    )

    if regex_factory_func is None:
        raise Exception(f"'{file_extension}' is not a recognized file extension.")

    # ----------------------------------------------------------------------
    def Replace(
        match: re.Match,
    ) -> str:
        return f"{match.group('opening_tag')}{new_content}{match.group('closing_tag')}"

    # ----------------------------------------------------------------------

    return regex_factory_func(tag_name).sub(Replace, content)


# ----------------------------------------------------------------------
def UpdateFile(
    filename: Path,
    replacment_info: dict[str, str],
) -> None:
    EnsureFile(filename)

    content = filename.read_text(encoding="utf-8")

    for tag_name, new_content in replacment_info.items():
        content = ReplaceContent(
            filename.suffix,
            tag_name,
            content,
            new_content,
        )

    # Ensure that we are always using unix line endings so that diffs work as expected during
    # updates (this is necessary because Jinja2 is configured to use unix line endings).
    filename.write_text(content, encoding="utf-8", newline="\n")


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
_regex_lookup: dict[tuple[str, ...], Callable[[str], Pattern]] = {
    (".htm", ".html", ".md"): lambda tag_name: re.compile(
        rf"""(?#
        Opening tag     )(?P<opening_tag>\<\!\-\-\s*\[BEGIN\]\s*{re.escape(tag_name)}\s*\-\-\>\s*?\r?\n)(?#
        Content         )(?P<content>.*?)(?#
        Closing tag     )(?P<closing_tag>\<\!\-\-\s*\[END\]\s*{re.escape(tag_name)}\s*\-\-\>\s*?\r?\n)(?#
        )""",
        re.DOTALL | re.MULTILINE,
    ),
}

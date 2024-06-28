import os
import re
import shutil
import textwrap

from enum import auto, Enum
from pathlib import Path
from typing import Match, Optional


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
            if filename in ["__preprocess.py", "__postprocess.py"]:
                continue

            source_filename = root / filename
            dest_filename = dest_dir / relative_path / filename

            shutil.move(source_filename, dest_filename)


# ----------------------------------------------------------------------
class AugmentFileStyle(Enum):
    """Controls how content is augmented"""

    # Replace the content or all the content within the tags
    Replace = auto()

    # Replace the content and remove the tags so that the content is not modified again
    Finalize = auto()

    # Append the content to the end of the file or end of the content within the tags
    Append = auto()

    # Prepend the content to the beginning of the file or beginning of the content within the tags
    Prepend = auto()


def AugmentFile(
    filename: Path,
    new_content: str,
    tag_name: Optional[str],
    augment_style: AugmentFileStyle = AugmentFileStyle.Append,
) -> None:
    if not filename.is_file():
        filename.parent.mkdir(parents=True, exist_ok=True)
        content = ""
    else:
        with filename.open(encoding="utf-8") as f:
            content = f.read()

    if tag_name:
        if filename.suffix in [
            ".htm",
            ".html",
            ".md",
        ]:
            regex = re.compile(
                rf"""(?#
                Opening tag     )(?P<opening_tag>\<\!\-\-\s*\[BEGIN\]\s*{re.escape(tag_name)}\s*\-\-\>\s*?\r?\n)(?#
                Content         )(?P<content>.*?)(?#
                Closing tag     )(?P<closing_tag>\<\!\-\-\s*\[END\]\s*{re.escape(tag_name)}\s*\-\-\>\s*?\r?\n)(?#
                )""",
                re.DOTALL | re.MULTILINE,
            )
        else:
            assert False, filename.suffix  # pragma: no cover

        # ----------------------------------------------------------------------
        def Sub(
            match: Match,
        ) -> str:
            if augment_style == AugmentFileStyle.Finalize:
                return new_content

            content = match.group("content")

            if augment_style == AugmentFileStyle.Replace:
                content = new_content
            elif augment_style == AugmentFileStyle.Append:
                content += new_content
            elif augment_style == AugmentFileStyle.Prepend:
                content = new_content + content
            else:
                assert False, augment_style  # pragma: no cover

            return f"{match.group('opening_tag')}{content}{match.group('closing_tag')}"

        # ----------------------------------------------------------------------

        content = regex.sub(Sub, content)

    else:
        if augment_style in [AugmentFileStyle.Replace, AugmentFileStyle.Finalize]:
            content = new_content
        elif augment_style == AugmentFileStyle.Append:
            content += new_content
        elif augment_style == AugmentFileStyle.Prepend:
            content = new_content + content
        else:
            assert False, augment_style  # pragma: no cover

    with filename.open("w", encoding="utf-8") as f:
        f.write(content)


# ----------------------------------------------------------------------
def CreateInstructionContent(
    title: str,
    steps_html: str,
) -> str:
    return textwrap.dedent(
        f"""\
        <details>
            <summary>
                <span role="term"><input type="checkbox" id="{title.lower().replace(' ', '-')}">{title}</span>
            </summary>
        </details>
        <div role="definition" class="details-content">
{steps_html}
        </div>
        """,
    )

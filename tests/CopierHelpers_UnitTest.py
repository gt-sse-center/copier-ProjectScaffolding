import os
import re
import sys
import textwrap

from pathlib import Path

import pytest

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx


# ----------------------------------------------------------------------
copier_helpers_filename = PathEx.EnsureExists(
    Path(__file__).parent.parent / "template" / "__tools" / "CopierHelpers.py"
)

sys.path.insert(0, str(copier_helpers_filename.parent))
with ExitStack(lambda: sys.path.pop(0)):
    from CopierHelpers import *


# ----------------------------------------------------------------------
class TestEnsureFile:
    # ----------------------------------------------------------------------
    def test_FileExists(self):
        EnsureFile(Path(__file__))
        assert True

    # ----------------------------------------------------------------------
    def test_FileDoesNotExist(self):
        invalid_filename = Path("file_does_not_exist.txt")

        with pytest.raises(
            ValueError,
            match=re.escape(f"'{invalid_filename}' is not a file."),
        ):
            EnsureFile(invalid_filename)


# ----------------------------------------------------------------------
class TestEnsureDir:
    # ----------------------------------------------------------------------
    def test_DirExists(self):
        EnsureDir(Path(__file__).parent)
        assert True

    # ----------------------------------------------------------------------
    def test_DirDoesNotExist(self):
        invalid_dir = Path("dir_does_not_exist")

        with pytest.raises(
            ValueError,
            match=re.escape(f"'{invalid_dir}' is not a directory."),
        ):
            EnsureDir(invalid_dir)


# ----------------------------------------------------------------------
class TestMoveFile:
    # ----------------------------------------------------------------------
    def test_StandardDir(self, fs):
        fs.create_file("template/file.txt")

        MoveFile(
            Path("template/file.txt"),
            Path("dest"),
        )

        assert _ListFiles(Path("dest")) == {"file.txt"}

    # ----------------------------------------------------------------------
    def test_NestedDir(self, fs):
        fs.create_file("template/file.txt")

        MoveFile(
            Path("template/file.txt"),
            Path("dest/nested/dir"),
        )

        assert _ListFiles(Path("dest")) == {"nested/dir/file.txt"}


# ----------------------------------------------------------------------
def test_MoveFiles(fs):
    fs.create_file("template/__postprocess.py")
    fs.create_file("template/File1.txt")
    fs.create_file("template/Dir1/File2.txt")
    fs.create_file("template/Dir1/__postprocess.py")
    fs.create_file("template/Dir1/Dir2/File3.txt")

    MoveFiles(
        Path("template"),
        Path("dest"),
    )

    assert _ListFiles(Path("dest")) == {
        "File1.txt",
        "Dir1/File2.txt",
        "Dir1/Dir2/File3.txt",
    }


# ----------------------------------------------------------------------
class TestReplaceContent:
    # ----------------------------------------------------------------------
    def test_Standard(self):
        assert (
            ReplaceContent(
                ".html",
                "Region Name",
                textwrap.dedent(
                    """\
                Before

                <!-- [BEGIN] Region Name -->
                <!-- [END] Region Name -->

                After
                """,
                ),
                textwrap.dedent(
                    """\
                    A
                    B
                    C
                    """,
                ),
            )
            == textwrap.dedent(
                """\
            Before

            <!-- [BEGIN] Region Name -->
            A
            B
            C
            <!-- [END] Region Name -->

            After
            """,
            )
        )

    # ----------------------------------------------------------------------
    def test_ErrorUnsupportedFile(self):
        with pytest.raises(
            Exception,
            match="'.foo' is not a recognized file extension.",
        ):
            ReplaceContent(
                ".foo",
                "Never used",
                "Never used",
                "Never used",
            )


# ----------------------------------------------------------------------
def test_UpdateFile(fs):
    filename = Path("my_filename.html")

    fs.create_file(
        filename,
        contents=textwrap.dedent(
            """\
            Before

            <!-- [BEGIN] Region 1 -->
            <!-- [END] Region 1 -->

            <!-- [BEGIN] Region 2 -->
            <!-- [END] Region 2 -->

            After
            """,
        ),
    )

    UpdateFile(
        filename,
        {
            "Region 1": "123\n",
            "Region 2": "abc\n",
        },
    )

    assert filename.read_text(encoding="utf-8") == textwrap.dedent(
        """\
        Before

        <!-- [BEGIN] Region 1 -->
        123
        <!-- [END] Region 1 -->

        <!-- [BEGIN] Region 2 -->
        abc
        <!-- [END] Region 2 -->

        After
        """,
    )

    filename_bytes = filename.read_bytes()

    assert "\n".encode() in filename_bytes
    assert "\r\n".encode() not in filename_bytes


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _ListFiles(
    path: Path,
) -> set[str]:
    result: set[str] = set()

    for root_str, _, filenames in os.walk(path):
        root = Path(root_str)

        relative_root = root.relative_to(path)

        for filename in filenames:
            result.add((relative_root / filename).as_posix())

    return result

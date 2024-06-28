import re
import sys
import textwrap
import uuid

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

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
    fs.create_file("template/__preprocess.py")
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
class TestAugmentFile:
    # ----------------------------------------------------------------------
    class TestAllContents:
        # ----------------------------------------------------------------------
        @staticmethod
        @contextmanager
        def YieldFile(fs) -> Iterator[Path]:
            file = Path("file.txt")

            file.unlink(missing_ok=True)
            fs.create_file(file, contents="Existing content\n")

            with ExitStack(file.unlink):
                yield file

        # ----------------------------------------------------------------------
        def test_Replace(self, fs):
            with self.__class__.YieldFile(fs) as file:
                AugmentFile(
                    file,
                    "This is the new content.\n",
                    None,
                    AugmentFileStyle.Replace,
                )

                assert file.read_text() == textwrap.dedent(
                    """\
                    This is the new content.
                    """,
                )

        # ----------------------------------------------------------------------
        def test_Finalize(self, fs):
            with self.__class__.YieldFile(fs) as file:
                AugmentFile(
                    file,
                    "This is the new content.\n",
                    None,
                    AugmentFileStyle.Finalize,
                )

                assert file.read_text() == textwrap.dedent(
                    """\
                    This is the new content.
                    """,
                )

        # ----------------------------------------------------------------------
        def test_Append(self, fs):
            with self.__class__.YieldFile(fs) as file:
                AugmentFile(
                    file,
                    "This is the new content.\n",
                    None,
                    AugmentFileStyle.Append,
                )

                assert file.read_text() == textwrap.dedent(
                    """\
                    Existing content
                    This is the new content.
                    """,
                )

        # ----------------------------------------------------------------------
        def test_Prepend(self, fs):
            with self.__class__.YieldFile(fs) as file:
                AugmentFile(
                    file,
                    "This is the new content.\n",
                    None,
                    AugmentFileStyle.Prepend,
                )

                assert file.read_text() == textwrap.dedent(
                    """\
                    This is the new content.
                    Existing content
                    """,
                )

    # ----------------------------------------------------------------------
    class TestTags:
        # ----------------------------------------------------------------------
        @staticmethod
        @contextmanager
        def YieldFile(fs) -> Iterator[Path]:
            file = Path("file.html")

            file.unlink(missing_ok=True)
            fs.create_file(
                file,
                contents=textwrap.dedent(
                    """\
                    Beginning Line

                    <!-- [BEGIN] Tag1 -->
                    Tag1 Line
                    <!-- [END] Tag1 -->

                    <!-- [BEGIN] Tag2 -->
                    Tag2 Line 1
                    Tag2 Line 2
                    <!-- [END] Tag2 -->

                    <!-- [BEGIN] Tag3 -->
                    Tag3 Line 1
                    Tag3 Line 2
                    Tag3 Line 3
                    <!-- [END] Tag3 -->

                    End Line
                    """,
                ),
            )

            with ExitStack(file.unlink):
                yield file

        # ----------------------------------------------------------------------
        def test_Replace(self, fs):
            with self.__class__.YieldFile(fs) as file:
                AugmentFile(
                    file,
                    textwrap.dedent(
                        """\
                        This is
                        the new
                        content.
                        """,
                    ),
                    "Tag2",
                    AugmentFileStyle.Replace,
                )

                assert file.read_text() == textwrap.dedent(
                    """\
                    Beginning Line

                    <!-- [BEGIN] Tag1 -->
                    Tag1 Line
                    <!-- [END] Tag1 -->

                    <!-- [BEGIN] Tag2 -->
                    This is
                    the new
                    content.
                    <!-- [END] Tag2 -->

                    <!-- [BEGIN] Tag3 -->
                    Tag3 Line 1
                    Tag3 Line 2
                    Tag3 Line 3
                    <!-- [END] Tag3 -->

                    End Line
                    """,
                )

        # ----------------------------------------------------------------------
        def test_Finalize(self, fs):
            with self.__class__.YieldFile(fs) as file:
                AugmentFile(
                    file,
                    textwrap.dedent(
                        """\
                        This is
                        the new
                        content.
                        """,
                    ),
                    "Tag2",
                    AugmentFileStyle.Finalize,
                )

                assert file.read_text() == textwrap.dedent(
                    """\
                    Beginning Line

                    <!-- [BEGIN] Tag1 -->
                    Tag1 Line
                    <!-- [END] Tag1 -->

                    This is
                    the new
                    content.

                    <!-- [BEGIN] Tag3 -->
                    Tag3 Line 1
                    Tag3 Line 2
                    Tag3 Line 3
                    <!-- [END] Tag3 -->

                    End Line
                    """,
                )

        # ----------------------------------------------------------------------
        def test_Append(self, fs):
            with self.__class__.YieldFile(fs) as file:
                AugmentFile(
                    file,
                    textwrap.dedent(
                        """\
                        This is
                        the new
                        content.
                        """,
                    ),
                    "Tag2",
                    AugmentFileStyle.Append,
                )

                assert file.read_text() == textwrap.dedent(
                    """\
                    Beginning Line

                    <!-- [BEGIN] Tag1 -->
                    Tag1 Line
                    <!-- [END] Tag1 -->

                    <!-- [BEGIN] Tag2 -->
                    Tag2 Line 1
                    Tag2 Line 2
                    This is
                    the new
                    content.
                    <!-- [END] Tag2 -->

                    <!-- [BEGIN] Tag3 -->
                    Tag3 Line 1
                    Tag3 Line 2
                    Tag3 Line 3
                    <!-- [END] Tag3 -->

                    End Line
                    """,
                )

        # ----------------------------------------------------------------------
        def test_Prepend(self, fs):
            with self.__class__.YieldFile(fs) as file:
                AugmentFile(
                    file,
                    textwrap.dedent(
                        """\
                        This is
                        the new
                        content.
                        """,
                    ),
                    "Tag2",
                    AugmentFileStyle.Prepend,
                )

                assert file.read_text() == textwrap.dedent(
                    """\
                    Beginning Line

                    <!-- [BEGIN] Tag1 -->
                    Tag1 Line
                    <!-- [END] Tag1 -->

                    <!-- [BEGIN] Tag2 -->
                    This is
                    the new
                    content.
                    Tag2 Line 1
                    Tag2 Line 2
                    <!-- [END] Tag2 -->

                    <!-- [BEGIN] Tag3 -->
                    Tag3 Line 1
                    Tag3 Line 2
                    Tag3 Line 3
                    <!-- [END] Tag3 -->

                    End Line
                    """,
                )

    # ----------------------------------------------------------------------
    def test_ExistingFile(self, fs):
        file = Path("existing_file.txt")

        file.unlink(missing_ok=True)
        fs.create_file(file, contents="Existing content\n")

        AugmentFile(
            file,
            "This is the new content\n",
            None,
            AugmentFileStyle.Append,
        )

        assert file.read_text() == textwrap.dedent(
            """\
            Existing content
            This is the new content
            """,
        )

    # ----------------------------------------------------------------------
    def test_NewFile(self, fs):
        # fs creates a fake file system, which monkey patches the existing file system. Do not
        # remove the parameter, even though it looks like it isn't being used.

        file = Path("new_file.txt")

        file.unlink(missing_ok=True)

        AugmentFile(
            file,
            "This is the new content\n",
            None,
            AugmentFileStyle.Append,
        )

        assert file.read_text() == textwrap.dedent(
            """\
            This is the new content
            """,
        )


# ----------------------------------------------------------------------
def test_CreateInstructionsContent():
    title = f"{str(uuid.uuid4())} suffix"
    steps_html = str(uuid.uuid4())

    assert CreateInstructionContent(title, steps_html) == textwrap.dedent(
        f"""\
        <details>
            <summary>
                <span role="term"><input type="checkbox" id="{title.replace(' ', '-')}">{title}</span>
            </summary>
        </details>
        <div role="definition" class="details-content">
{steps_html}
        </div>
        """,
    )


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

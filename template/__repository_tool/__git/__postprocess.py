import sys
import textwrap

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
def UpdateGitIgnore():
    gitignore_filename = EnsureFile(Path.cwd() / ".gitignore")

    if "{{ project_type }}" in ["PythonExecutionEnvironment", "PythonPackage"]:
        with gitignore_filename.open("a") as f:
            f.write(
                textwrap.dedent(
                    """\

                    Activate*.cmd
                    Activate*.sh
                    Deactivate*.cmd
                    Deactivate*.sh

                    **/__pycache__/**
                    **/Generated/**
                    """,
                ),
            )

    if "{{ project_type }}" == "PythonPackage":
        with gitignore_filename.open("a") as f:
            f.write(
                textwrap.dedent(
                    """\

                    **/.coverage
                    **/lcov.info
                    **/.vscode

                    build/**
                    dist/**
                    src/{{ python_package_pypi_name }}.egg-info/**
                    """,
                ),
            )

    if "{{ python_package_generate_ci_sign_artifacts }}".lower() == "true":
        with gitignore_filename.open("a") as f:
            f.write(
                textwrap.dedent(
                    """\

                    minisign_key.pri
                    """,
                ),
            )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    UpdateGitIgnore()

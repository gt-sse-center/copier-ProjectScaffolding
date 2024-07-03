import sys
import subprocess
import textwrap

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()
python_bootstrapper_dir = EnsureDir(output_dir / "__tools" / "__python_bootstrapper")

MoveFiles(python_bootstrapper_dir, output_dir)

subprocess.run(
    f'python "{EnsureFile(python_bootstrapper_dir / "__preprocess.py")}"',
    check=True,
    shell=True,
)

{% if repository_tool == 'git' %}
AugmentFile(
    EnsureFile(output_dir / ".gitignore"),
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
    None,
)

{% endif %}


# ----------------------------------------------------------------------
# |
# |  Documentation
# |
# ----------------------------------------------------------------------
{% if generate_docs %}

# ----------------------------------------------------------------------
readme_filename = EnsureFile(output_dir / "README.md")

pip_instructions = textwrap.dedent(
    """\
    ### Installation via pip
    To install the {{ project_name }} package via [pip](https://pip.pypa.io/en/stable/) (Python Installer for Python) for use with your python code:

    `pip install {{ python_package_pypi_name }}`
    """,
)

{% if hosting_platform == 'None' %}
installation_instructions = pip_instructions
{% elif hosting_platform == 'GitHub' %}
installation_instructions = textwrap.dedent(
    """\
    {{ project_name }} can be installed via one of these methods:

    - [Installation via Executable](#installation-via-executable)
    - [Installation via pip](#installation-via-pip)

    ### Installation via Executable
    Download an executable for Linux, MacOS, or Windows to the the functionality provided by this repository without a dependency on python.

    1. Download the archive for the latest release [here]({{ github_url }}/releases/latest). The filename will begin with `exe.` and contain the name of your operating system.
    2. Decompress the archive.

    {}
    """,
).format(pip_instructions)
{% else %}
{{ "Define this section for your 'hosting_platform'." | raise_exception }}
{% endif %}

AugmentFile(
    readme_filename,
    installation_instructions,
    "Installation",
    AugmentFileStyle.Finalize,
)


# ----------------------------------------------------------------------
development_filename = EnsureFile(output_dir / "DEVELOPMENT.md")

AugmentFile(
    development_filename,
    textwrap.dedent(
        """\
        Each of these activities can be invoked from an activated terminal on your local machine.

        | Activity | Command Line | Description | Invoked by Continuous Integration |
        | --- | --- | --- | --- |
        | Code Formatting | `python Build.py black [--format]` | Format source code using [black](https://github.com/psf/black) based on settings in `pyproject.toml`. | |
        | Static Code Analysis | `python Build.py pylint` | Validate source code using [pylint](https://github.com/pylint-dev/pylint) based on settings in `pyproject.toml`. | |
        | Automated Testing | `python Build.py pytest [--code-coverage]` | Run automated tests using [pytest](https://docs.pytest.org/) and (optionally) extract code coverage information using [coverage](https://coverage.readthedocs.io/) based on settings in `pyproject.toml`. | |
        | Semantic Version Generation | `python Build.py update_version` | Generate a new [Semantic Version](https://semver.org) based on git commits using [AutoGitSemVer](https://github.com/davidbrownell/AutoGitSemVer). Version information is stored in `/src/{{ python_package_pypi_name }}/__init__.py`. | |
        | Python Package Creation | <p><code>python Build.py package</code></p><p>Requires that the repository was bootstrapped with the <code>--package</code> flag. | Create a python package using [setuptools](https://github.com/pypa/setuptools) based on settings in `pyproject.toml`. | |
        | Python Package Publishing | <p><code>python Build.py publish</code></p><p>Requires that the repository was bootstrapped with the <code>--package</code> flag. | Publish a python package to [PyPi](https://pypi.org). | |
        | Build Binaries | `python Build.py build_binaries` |  Create a python binary for your current operating system using [cx_Freeze](https://cx-freeze.readthedocs.io/) based on settings in `src/BuildBinary.py`. | |
        | Development Docker Image | `python Build.py create_docker_image` | Create a [docker](https://docker.com) image for a bootstrapped development environment. This functionality is useful when adhering to the [FAIR principles for research software](https://doi.org/10.1038/s41597-022-01710-x) by supporting the creation of a development environment and its dependencies as they existed at the moment when the image was created. | |
        """,
    ),
    "Development Activities",
    AugmentFileStyle.Finalize,
)

{% endif %}

# ----------------------------------------------------------------------
# |
# |  post_generation_actions.html
# |
# ----------------------------------------------------------------------
post_generation_actions_filename = EnsureFile(output_dir / "post_generation_actions.html")

AugmentFile(
    post_generation_actions_filename,
    CreateInstructionContent(
        "Update pyproject.toml",
        textwrap.dedent(
            """\
            <p>Python development tools, package dependencies, and packaging instructions are configured in <code>pyproject.toml</code>. Please visit <a href="https://packaging.python.org/en/latest/guides/writing-pyproject-toml/" target="_blank">this link</a> for more information on these files.</p>
            <p>Please search for and replace all <code>TODO:</code> comments in <code>pyproject.toml</code>.</p>
            """,
        ),
    ),
    "After Repository Tool Instruction",
)

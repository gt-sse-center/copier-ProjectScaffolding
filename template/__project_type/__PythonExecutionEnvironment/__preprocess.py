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


# ----------------------------------------------------------------------
# |
# |  Documentation
# |
# ----------------------------------------------------------------------
{% if generate_docs %}

# ----------------------------------------------------------------------
readme_filename = EnsureFile(output_dir / "README.md")

AugmentFile(
    readme_filename,
    "",
    "Badges",
    AugmentFileStyle.Finalize,
)

AugmentFile(
    readme_filename,
    "No additional setup is required to use this project.\n",
    "Installation",
    AugmentFileStyle.Finalize,
)


# ----------------------------------------------------------------------
development_filename = EnsureFile(output_dir / "DEVELOPMENT.md")

# The enlistment section will have been populated by __tools/__python_bootstrapper/__preprocess.py

AugmentFile(
    development_filename,
    "TODO: Complete this section\n",
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
    "",
    "Before Repository Tool Instruction",
    AugmentFileStyle.Finalize,
)

AugmentFile(
    post_generation_actions_filename,
    CreateInstructionContent(
        "Update requirements.txt",
        textwrap.dedent(
            """\
            <p>Python package dependencies can be added to <code>requirements.txt</code>. These packages will be automatically installed when the environment is <a href="https://github.com/davidbrownell/PythonBootstrapper" target="_blank">bootstrapped</a>.</p>
            <p>Please visit <a href="https://pip.pypa.io/en/stable/reference/requirements-file-format/" target="_blank">this link</a> for more information on requirements files and how they can be used.</p>
            """,
        ),
    ),
    "After Repository Tool Instruction",
)

AugmentFile(
    post_generation_actions_filename,
    CreateInstructionContent(
        "Update DEVELOPMENT.md",
        textwrap.dedent(
            """\
            <p>Please search for and replace all <code>TODO:</code> comments in <code>DEVELOPMENT.md</code>.</p>
            """,
        ),
    ),
    "After Repository Tool Instruction",
)

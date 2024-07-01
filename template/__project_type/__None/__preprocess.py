import sys

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()

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
    "TODO: Complete this section\n",
    "Installation",
    AugmentFileStyle.Finalize,
)


# ----------------------------------------------------------------------
development_filename = EnsureFile(output_dir / "DEVELOPMENT.md")

AugmentFile(
    development_filename,
    "TODO: Complete this section\n",
    "Enlistment",
    AugmentFileStyle.Finalize,
)

AugmentFile(
    development_filename,
    "TODO: Complete this section\n",
    "Development Activities",
    AugmentFileStyle.Finalize,
)

{% endif %}


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
    "",
    "After Repository Tool Instruction",
    AugmentFileStyle.Finalize,
)

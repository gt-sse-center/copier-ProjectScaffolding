import sys

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()


# ----------------------------------------------------------------------
# |
# |  post_generation_actions.html
# |
# ----------------------------------------------------------------------
AugmentFile(
    EnsureFile(output_dir / "post_generation_actions.html"),
    "",
    "Repository Tool Instruction",
    AugmentFileStyle.Finalize,
)

import sys

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
def MoveContent():
    output_dir = Path.cwd()
    python_bootstrapper_dir = EnsureDir(output_dir / "__tools" / "__python_bootstrapper")

    MoveFiles(python_bootstrapper_dir, output_dir)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    MoveContent()

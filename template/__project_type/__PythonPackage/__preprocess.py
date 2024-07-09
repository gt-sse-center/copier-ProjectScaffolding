import sys
import subprocess

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()
python_bootstrapper_dir = EnsureDir(output_dir / "__tools" / "__python_bootstrapper")

subprocess.run(
    f'python "{EnsureFile(python_bootstrapper_dir / "__preprocess.py")}"',
    check=True,
    shell=True,
)

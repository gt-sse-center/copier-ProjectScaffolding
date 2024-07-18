import sys
import subprocess

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()
hosting_platform_dir = output_dir / "__hosting_platform" / "__{{ hosting_platform }}"

if hosting_platform_dir.is_dir():
    MoveFiles(hosting_platform_dir, output_dir)

    preprocess_filename = hosting_platform_dir / "__postprocess.py"
    if preprocess_filename.is_file():
        subprocess.run(
            f'python "{preprocess_filename}"',
            check=True,
            shell=True,
        )

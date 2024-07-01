import sys
import subprocess

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()
project_type_dir = EnsureDir(output_dir / "__project_type" / "__{{ project_type }}")
preprocess_filename = project_type_dir / "__preprocess.py"

MoveFiles(project_type_dir, output_dir)

if preprocess_filename.is_file():
    subprocess.run(
        f'python "{preprocess_filename}"',
        check=True,
        shell=True,
    )

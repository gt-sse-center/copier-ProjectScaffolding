import sys
import subprocess

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()
repository_tool_dir = output_dir / "__repository_tool" / "__{{ repository_tool }}"

if repository_tool_dir.is_dir():
    MoveFiles(repository_tool_dir, output_dir)

    preprocess_filename = repository_tool_dir / "__preprocess.py"
    if preprocess_filename.is_file():
        subprocess.run(
            f'python "{preprocess_filename}"',
            check=True,
            shell=True,
        )

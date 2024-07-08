import sys
import subprocess

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()
repository_tool_dir = EnsureDir(output_dir / "__repository_tool" / "__{{ repository_tool }}")
preprocess_filename = repository_tool_dir / "__preprocess.py"

MoveFiles(repository_tool_dir, output_dir)

if preprocess_filename.is_file():
    subprocess.run(
        f'python "{preprocess_filename}"',
        check=True,
        shell=True,
    )

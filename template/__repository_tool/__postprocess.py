import sys
import subprocess

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()
repository_tool_dir = EnsureDir(output_dir / "__repository_tool" / "__{{ repository_tool }}")
postprocess_filename = repository_tool_dir / "__postprocess.py"

if postprocess_filename.is_file():
    subprocess.run(
        f'python "{postprocess_filename}"',
        check=True,
        shell=True,
    )

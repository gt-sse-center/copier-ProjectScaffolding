import sys

{% if repository_tool == 'None' %}
sys.exit()
{% endif %}

import subprocess

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
this_dir = Path.cwd()
repository_tool_dir = EnsureDir(this_dir / "__repository_tool")
postprocess_filename = repository_tool_dir / "__{{ repository_tool }}" / "__postprocess.py"

if postprocess_filename.is_file():
    subprocess.run(
        f'python "{postprocess_filename}"',
        check=True,
        shell=True,
    )

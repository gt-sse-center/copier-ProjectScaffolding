import sys

{% if hosting_platform == 'None' %}
sys.exit()
{% endif %}

import subprocess

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()
hosting_platform_dir = EnsureDir(output_dir / "__hosting_platform" / "__{{ hosting_platform }}")
preprocess_filename = hosting_platform_dir / "__preprocess.py"

MoveFiles(hosting_platform_dir, output_dir)

if preprocess_filename.is_file():
    subprocess.run(
        f'python "{preprocess_filename}"',
        check=True,
        shell=True,
    )

import sys

{% if hosting_platform == 'None' %}
sys.exit()
{% endif %}

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
this_dir = Path.cwd()
hosting_platform_dir = EnsureDir(this_dir / "__hosting_platform")

MoveFiles(EnsureDir(hosting_platform_dir / "__{{ hosting_platform }}"), this_dir)

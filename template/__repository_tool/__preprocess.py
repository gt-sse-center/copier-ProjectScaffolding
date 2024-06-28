import sys

{% if repository_tool == 'None' %}
sys.exit()
{% endif %}

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
this_dir = Path.cwd()
repository_tool_dir = EnsureDir(this_dir / "__repository_tool")

MoveFiles(EnsureDir(repository_tool_dir / "__{{ repository_tool }}"), this_dir)

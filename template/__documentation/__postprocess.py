import sys

{% if not generate_docs %}
sys.exit()
{% endif %}

import shutil

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
this_dir = Path.cwd()

documentation_dir = EnsureDir(this_dir / "__documentation")


# ----------------------------------------------------------------------
licenses_dir = EnsureDir(documentation_dir / "__licenses")

{% if documentation_license != 'None' %}
MoveFile(
    EnsureFile(licenses_dir / "{{ documentation_license }}_LICENSE.txt"),
    documentation_dir,
    "LICENSE.txt",
)
{% endif %}

shutil.rmtree(licenses_dir)

MoveFiles(documentation_dir, this_dir)

# BugBug: Add rest of documentation

import sys

{% if not generate_docs %}
sys.exit()
{% endif %}

import shutil

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()

documentation_dir = EnsureDir(output_dir / "__documentation")


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

MoveFiles(documentation_dir, output_dir)


# ----------------------------------------------------------------------
# |
# |  post_generation_actions.html
# |
# ----------------------------------------------------------------------
post_generation_actions_filename = EnsureFile(output_dir / "post_generation_actions.html")

AugmentFile(
    post_generation_actions_filename,
    CreateInstructionContent(
        "Update README.md",
        textwrap.dedent(
            """\
            <p>Please search for and replace all <code>TODO:</code> comments in <code>README.md</code>.</p>
            """,
        ),
    ),
    "After Repository Tool Instruction",
)

post_generation_actions_filename = EnsureFile(output_dir / "post_generation_actions.html")

AugmentFile(
    post_generation_actions_filename,
    CreateInstructionContent(
        "Update MAINTAINERS.md",
        textwrap.dedent(
            """\
            <p>Please search for and replace all <code>TODO:</code> comments in <code>MAINTAINERS.md</code>.</p>
            """,
        ),
    ),
    "After Repository Tool Instruction",
)

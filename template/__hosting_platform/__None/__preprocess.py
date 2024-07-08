import sys
import textwrap

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()


# ----------------------------------------------------------------------
# |
# |  Documentation
# |
# ----------------------------------------------------------------------
{% if generate_docs %}

# ----------------------------------------------------------------------
contributing_filename = EnsureFile(output_dir / "CONTRIBUTING.md")

AugmentFile(
    contributing_filename,
    "TODO: Include information on how to submit pull requests and/or issues.\n",
    "General Information",
    AugmentFileStyle.Finalize,
)

AugmentFile(
    contributing_filename,
    "TODO: Include information on how to use branches effectively and create a pull request.\n",
    "Pull Requests and Branches",
    AugmentFileStyle.Finalize,
)

AugmentFile(
    contributing_filename,
    "TODO: Include information on how proposals are handled.\n",
    "Proposals",
    AugmentFileStyle.Finalize,
)


# ----------------------------------------------------------------------
security_filename = EnsureFile(output_dir / "SECURITY.md")

AugmentFile(
    security_filename,
    "TODO: Include information on how to securely submit a vulnerability.\n",
    "Submit Vulnerability",
    AugmentFileStyle.Finalize,
)

{% endif %}

# ----------------------------------------------------------------------
# |
# |  post_generation_actions.html
# |
# ----------------------------------------------------------------------
{% if generate_docs %}

post_generation_actions_filename = EnsureFile(output_dir / "post_generation_actions.html")

AugmentFile(
    post_generation_actions_filename,
    CreateInstructionContent(
        "Update CONTRIBUTING.md",
        textwrap.dedent(
            """\
            <p>Please search for and replace all <code>TODO:</code> comments in <code>CONTRIBUTING.md</code>.</p>
            """,
        ),
    ),
    "After Repository Tool Instruction",
)

AugmentFile(
    post_generation_actions_filename,
    CreateInstructionContent(
        "Update SECURITY.md",
        textwrap.dedent(
            """\
            <p>Please search for and replace all <code>TODO:</code> comments in <code>SECURITY.md</code>.</p>
            """,
        ),
    ),
    "After Repository Tool Instruction",
)

{% endif %}

import sys
import textwrap

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()


# ----------------------------------------------------------------------
# Create the instructions specific to git for inclusion in post_generation_actions.html.

# Start by reading the filenames found in __git_precommit_permissions.txt. These are the files whose
# permissions need to be changed to allow execution.
precommit_permissions_filename = EnsureFile(output_dir / "__git_precommit_permissions.txt")

precommit_permissions = precommit_permissions_filename.read_text(encoding="utf-8").strip()

commit_step_num = 2
push_step_num = 3

if precommit_permissions:
    precommit_permissions_lines = [line.strip() for line in precommit_permissions.splitlines() if line.strip()]

    precommit_permissions = "{}<br/>\n".format("<br/>\n".join(f'{commit_step_num + index}. <code>git update-index --chmod=+x "{line}</code>"' for index, line in enumerate(precommit_permissions_lines)))

    commit_step_num += len(precommit_permissions_lines)
    push_step_num += len(precommit_permissions_lines)

actions_content = textwrap.dedent(
    """\
    <p>In this step, we will commit the files generated in git and push the changes.</p>

    <p>Open a terminal window, navigate to <code>{working_dir}</code>, and run the following commands:</p>

    1. <code>git add --all</code><br/>
    {precommit_permissions}{commit_step_num}. <code>git commit -m "🎉 Initial commit"</code><br/>
    {push_step_num}. <code>git push</code><br/>
    </p>
    """,
).format(
    working_dir=Path.cwd(),
    precommit_permissions=precommit_permissions,
    commit_step_num=commit_step_num,
    push_step_num=push_step_num,
)

AugmentFile(
    EnsureFile(output_dir / "post_generation_actions.html"),
    CreateInstructionContent("Initialize the git repository", actions_content),
    "Repository Tool Instruction",
    AugmentFileStyle.Finalize,
)

precommit_permissions_filename.unlink()

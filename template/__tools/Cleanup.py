import shutil
import sys
import textwrap

from pathlib import Path


# ----------------------------------------------------------------------
sys.stdout.write(
    "\n".join(
        f"        {line}" for line in
        textwrap.dedent(
            """\


            Code Generation is complete!

                Repository Tool:    {{ repository_tool }}
                Hosting Platform:   {{ hosting_platform }}
                Project Type:       {{ project_type }}

            Please open the file:

                ./post_generation_actions.html

            to complete the steps that must be finished before this repository can be used.


            """,
        ).split("\n")
    ),
)
sys.stdout.write("\n")


# ----------------------------------------------------------------------
shutil.rmtree("__documentation")
shutil.rmtree("__hosting_platform")
shutil.rmtree("__post_generation_actions")
shutil.rmtree("__project_type")
shutil.rmtree("__repository_tool")
Path("AutoGitSemVer.yaml").unlink()

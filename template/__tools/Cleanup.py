import shutil

from pathlib import Path


# ----------------------------------------------------------------------
shutil.rmtree("__documentation")
shutil.rmtree("__hosting_platform")
shutil.rmtree("__post_generation_actions")
shutil.rmtree("__project_type")
shutil.rmtree("__repository_tool")
Path("AutoGitSemVer.yaml").unlink()

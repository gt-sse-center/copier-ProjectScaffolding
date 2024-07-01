{% if not _disable_git_directory_check %}
import sys

from pathlib import Path


# ----------------------------------------------------------------------
git_dir = Path.cwd() / ".git"

if not git_dir.is_dir():
    sys.stderr.write(f"\nERROR: A '.git' directory does not exist at '{git_dir}'. Please generate the project into a directory that is an existing git repository.\n\n")
    sys.exit(-1)

{% endif %}

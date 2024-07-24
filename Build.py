"""Build tasks for this project."""

import sys

from pathlib import Path

import typer

from dbrownell_Common import PathEx
from dbrownell_DevTools.RepoBuildTools import Python as RepoBuildTools
from typer.core import TyperGroup


# ----------------------------------------------------------------------
class NaturalOrderGrouper(TyperGroup):
    # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def list_commands(self, *args, **kwargs):  # pylint: disable=unused-argument
        return self.commands.keys()


# ----------------------------------------------------------------------
app = typer.Typer(
    cls=NaturalOrderGrouper,
    help=__doc__,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
)


# ----------------------------------------------------------------------
this_dir = PathEx.EnsureDir(Path(__file__).parent)


# ----------------------------------------------------------------------
Black = RepoBuildTools.BlackFuncFactory(this_dir, app)

Pytest = RepoBuildTools.PytestFuncFactory(
    this_dir,
    "code_coverage_does_not_apply_to_this_repo",
    app,
    default_min_coverage=0.0,
)

CreateDockerImage = RepoBuildTools.CreateDockerImageFuncFactory(this_dir, app)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(app())

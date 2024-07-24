"""Build tasks for the docker image."""

import sys

from pathlib import Path
from typing import Annotated, Optional

import typer

from dbrownell_Common.Streams.DoneManager import DoneManager, Flags as DoneManagerFlags
from dbrownell_Common import SubprocessEx
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
@app.command("build", no_args_is_help=False)
def Build(
    image_name: Annotated[Optional[str], typer.Argument(help="Name of the docker image.")] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Write verbose information to the terminal."),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option("--debug", help="Write debug information to the terminal."),
    ] = False,
) -> None:
    """Builds the docker image."""

    with DoneManager.CreateCommandLine(
        flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        with dm.Nested("Building docker image...") as build_dm:
            command_line = "docker build --tag {} .".format(
                image_name or "copier-projectscaffolding"
            )

            build_dm.WriteVerbose(f"Command Line: {command_line}\n\n")

            with build_dm.YieldStream() as stream:
                build_dm.result = SubprocessEx.Stream(
                    command_line,
                    stream,
                    cwd=Path(__file__).parent,
                )

                if build_dm.result != 0:
                    return


# ----------------------------------------------------------------------
@app.command("publish", no_args_is_help=True)
def Publish(
    image_name: Annotated[str, typer.Argument(help="Name of the docker image previously built.")],
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Write verbose information to the terminal."),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option("--debug", help="Write debug information to the terminal."),
    ] = False,
) -> None:
    """Publishes the docker image to docker hub."""

    with DoneManager.CreateCommandLine(
        flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        with dm.Nested(f"Publishing '{image_name}'...") as publish_dm:
            command_line = f"docker push {image_name}"

            publish_dm.WriteVerbose(f"Command Line: {command_line}\n\n")

            with publish_dm.YieldStream() as stream:
                publish_dm.result = SubprocessEx.Stream(
                    command_line,
                    stream,
                    cwd=Path(__file__).parent,
                )

                if publish_dm.result != 0:
                    return


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(app())

import shutil

from pathlib import Path
from typing import Annotated

import rtyaml
import typer

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx
from dbrownell_Common.Streams.DoneManager import DoneManager, Flags as DoneManagerFlags
from dbrownell_Common import SubprocessEx
from typer.core import TyperGroup

import TestHelpers


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
@app.command("EntryPoint", no_args_is_help=True)
def EntryPoint(
    output_dir: Annotated[
        Path,
        typer.Argument(
            file_okay=False, resolve_path=True, help="The directory where output will be written."
        ),
    ],
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Write verbose information to the terminal."),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option("--debug", help="Write debug information to the terminal."),
    ] = False,
) -> None:
    """Generates all permutations of the templates to an output directory. Doing this makes it easier to validate the output of each configuration."""

    with DoneManager.CreateCommandLine(
        flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        parent_dir = Path(__file__).parent.parent

        command_line_template = f'copier copy "{parent_dir}" "{{output_dir}}" --trust --overwrite --defaults --data-file "{{data_file}}"'

        for configuration_info in TestHelpers.ConfigurationInfo.Generate():
            with dm.Nested(f"Generating '{configuration_info.name}'...", suffix="\n") as this_dm:
                configuration_filename = PathEx.CreateTempFileName(".yaml")

                with configuration_filename.open("w") as f:
                    rtyaml.dump(configuration_info.configuration, f)

                with ExitStack(configuration_filename.unlink):
                    this_output_dir = output_dir / configuration_info.name
                    if this_output_dir.is_dir():
                        shutil.rmtree(this_output_dir)

                    command_line = command_line_template.format(
                        output_dir=output_dir / configuration_info.name,
                        data_file=configuration_filename,
                    )

                    this_dm.WriteVerbose(f"Command Line: {command_line}\n\n")

                    with this_dm.YieldStream() as stream:
                        this_dm.result = SubprocessEx.Stream(command_line, stream, parent_dir)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()

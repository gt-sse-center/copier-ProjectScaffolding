import sys

from pathlib import Path
from typing import Any

from copier_templates_extensions import ContextHook
from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common import SubprocessEx


# ----------------------------------------------------------------------
class ContextUpdater(ContextHook):
    """Class that handles the generation of dynamic values."""

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        super(ContextUpdater, self).__init__(*args, **kwargs)

        self._updated_context: dict[str, Any] | None = None
        self._dest_path: Path | None = None
        self._is_update_temp_dir: bool | None = None

    # ----------------------------------------------------------------------
    def hook(self, context):
        # This method is invoked once for each template file being processed. Populate
        # the dynamic values when this is called for the first template file, and return
        # those dynamically generated values for all subsequent template files.
        if self._updated_context is None:
            assert self._dest_path is None
            assert self._is_update_temp_dir is None

            self._updated_context = {}
            self._dest_path = Path(context["_copier_conf"]["dst_path"])
            self._dest_path.mkdir(parents=True, exist_ok=True)

            # During update, copier will fully generate different template versions to local
            # directories and then create a diff for all changes between those generated
            # directories. These diffs are then applied to the actual directory.
            #
            # We don't want the dynamic context steps to be invoked when generating the temporary
            # directories, as the steps will generate different values in each, which will result
            # in a diff applied to the actual directory that contains the dynamic values.
            #
            # Detect when we are in this scenario and ensure the dynamic values are populated with
            # the same placeholder values so that they don't result in a diff.
            self._is_update_temp_dir = context["_folder_name"].startswith("copier.main")

            self._GeneratePythonPackageGistId(context)
            self._GeneratePythonPackageMinisignKey(context)

        assert self._updated_context is not None
        assert self._dest_path is not None
        assert self._is_update_temp_dir is not None

        return self._updated_context

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def _GeneratePythonPackageGistId(self, context) -> None:
        if not context["python_package_generate_ci_persist_coverage"]:
            return

        if self._is_update_temp_dir or context.get(
            "_python_package_generate_ci_persist_coverage_simulate_gist_id", False
        ):
            assert self._updated_context is not None

            self._updated_context["python_package_generate_ci_persist_coverage_gist_id"] = (
                "__simulated_gist_id__"
            )
            self._updated_context["python_package_generate_ci_persist_coverage_gist_username"] = (
                "__simulated_gist_username__"
            )

    # ----------------------------------------------------------------------
    def _GeneratePythonPackageMinisignKey(self, context) -> None:
        if not context["python_package_generate_ci_sign_artifacts"]:
            return

        if self._is_update_temp_dir or context.get(
            "_python_package_generate_ci_sign_artifacts_simulate_keygen", False
        ):
            public_key = "__simulated_minisign_public_key__"
        else:
            assert self._dest_path is not None
            public_key_filename = self._dest_path / "minisign_key.pub"

            # Create the key (if necessary)
            if not public_key_filename.is_file():
                with DoneManager.Create(
                    sys.stdout,
                    "\n\nCreating the Minisign public and private keys...",
                    suffix="\n\n\n",
                ) as dm:
                    command_line = 'docker run -i --rm -v ".:/host" jedisct1/minisign -G -p /host/minisign_key.pub -s /host/minisign_key.pri -W'

                    dm.WriteInfo(f"Command Line: {command_line}\n\n")

                    with dm.YieldStream() as stream:
                        dm.result = SubprocessEx.Stream(
                            command_line,
                            stream,
                            cwd=self._dest_path,
                        )
                        if dm.result != 0:
                            sys.exit(dm.result)

                assert public_key_filename.is_file(), public_key_filename

            # Read the public key
            key_lines = [
                line.strip()
                for line in public_key_filename.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            public_key = key_lines[-1]

        assert self._updated_context is not None
        self._updated_context["python_package_generate_ci_sign_artifacts_public_key"] = public_key

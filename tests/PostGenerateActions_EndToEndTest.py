import copy

import pytest

from dbrownell_Common import SubprocessEx

from TestHelpers import *


# ----------------------------------------------------------------------
def _IsDockerAvailable() -> bool:
    result = SubprocessEx.Run("docker --version")
    return result.returncode == 0


# ----------------------------------------------------------------------
@pytest.mark.skipif(not _IsDockerAvailable(), reason="Docker is not available")
def test_MinisignKeyGeneration(copie):
    configuration_info = next(
        copy.deepcopy(ci)
        for ci in ConfigurationInfo.Generate()
        if ci.configuration["generate_docs"]
        and ci.configuration.get("python_package_generate_ci_sign_artifacts_question", False)
    )

    del configuration_info.configuration[
        "_python_package_generate_ci_sign_artifacts_simulate_keygen"
    ]

    output_dir = RunTest(
        copie,
        configuration_info.configuration,
    )

    assert output_dir is not None

    public_key_filename = output_dir / "minisign_key.pub"
    private_key_filename = output_dir / "minisign_key.pri"

    assert public_key_filename.is_file(), public_key_filename
    assert private_key_filename.is_file(), private_key_filename

    public_key_lines = [
        line.strip()
        for line in public_key_filename.read_text(encoding="utf-8").split("\n")
        if line.strip()
    ]
    public_key_content = public_key_lines[-1]

    readme_content = (output_dir / "README.md").read_text(encoding="utf-8")

    assert public_key_content in readme_content

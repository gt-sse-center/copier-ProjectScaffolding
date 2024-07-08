import pytest

from TestHelpers import *


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_NoGit(copie):
    configuration_info = next(
        ci for ci in ConfigurationInfo.Generate() if ci.configuration["repository_tool"] == "git"
    )

    configuration_info.configuration["_git_disable_directory_check"] = False

    RunTest(
        copie,
        configuration_info.configuration,
        expect_failure=True,
    )

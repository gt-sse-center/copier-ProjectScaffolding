import copy

import pytest

from TestHelpers import *


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_GitHubWithoutGit(copie):
    configuration_info = next(
        copy.deepcopy(ci)
        for ci in ConfigurationInfo.Generate(include_invalid=True)
        if ci.configuration["repository_tool"] != "git"
        and ci.configuration["hosting_platform"] == "GitHub"
    )

    RunTest(
        copie,
        configuration_info.configuration,
        expect_failure=True,
    )

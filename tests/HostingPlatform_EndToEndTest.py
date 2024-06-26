import pytest

from TestHelpers import *


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
@pytest.mark.parametrize(
    "hosting_platform",
    [
        "None",
        "GitHub",
    ],
)
def test_GitHub(hosting_platform, copie, configuration, snapshot):
    configuration["hosting_platform"] = hosting_platform

    RunTest(
        copie,
        configuration,
        snapshot,
        include_globs={".github/**/*.*"},
    )

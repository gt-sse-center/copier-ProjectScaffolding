import pytest

from TestHelpers import *


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
@pytest.mark.parametrize(
    "project_type",
    [
        "None",
        "PythonExecutionEnvironment",
    ],
)
@pytest.mark.parametrize(
    "hosting_platform",
    [
        "None",
        "GitHub",
    ],
)
@pytest.mark.parametrize(
    "repository_tool",
    [
        "None",
        "git",
    ],
)
def test_Files(repository_tool, hosting_platform, project_type, copie, configuration, snapshot):
    configuration["repository_tool"] = repository_tool
    configuration["hosting_platform"] = hosting_platform
    configuration["project_type"] = project_type
    configuration["generate_docs"] = False

    expect_failure = hosting_platform == "GitHub" and repository_tool != "git"

    RunTest(
        copie,
        configuration,
        snapshot,
        exclude_globs={
            "post_generation_actions.html",
        },
        expect_failure=expect_failure,
    )

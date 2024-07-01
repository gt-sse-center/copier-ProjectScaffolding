import pytest

from TestHelpers import *


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_NoGitDirectoryError(copie, configuration):
    del configuration["_disable_git_directory_check"]

    RunTest(
        copie,
        configuration,
        None,
        expect_failure=True,
    )

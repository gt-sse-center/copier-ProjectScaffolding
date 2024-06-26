import re

from datetime import datetime

import pytest

from TestHelpers import *


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
@pytest.mark.parametrize(
    "license",
    [
        "None",
        "Apache-2.0",
        "BSD-3-Clause-Clear",
        "BSL-1.0",
        "GPL-3.0-or-later",
        "MIT",
    ],
)
def test_License(license, copie, configuration, snapshot):
    configuration["documentation_license"] = license

    output = RunTest(
        copie,
        configuration,
        snapshot,
        include_globs={"LICENSE.txt"},
    )

    if license != "None":
        license_content = output["LICENSE.txt"]

        assert re.search(
            rf"""(?#
            Beginning of line   )^(?#
            Copyright           )Copyright\s+(?#
            Mark                )(?:\([cC]\)\s+)?(?#
            Year                ){datetime.now().year}\s+(?#
            Project Name        )<<project_name>>(?#
            End of line         )$(?#
            )""",
            license_content,
            re.MULTILINE,
        )


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
@pytest.mark.parametrize(
    "hosting_platform",
    [
        "None",
        "GitHub",
    ],
)
@pytest.mark.parametrize(
    "filename",
    [
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        # TODO: "DEVELOPMENT.md",
        "GOVERNANCE.md",
        "MAINTAINERS.md",
        # TODO: "README.md",
        "SECURITY.md",
    ],
)
def test_Document(filename, hosting_platform, copie, configuration, snapshot):
    configuration["hosting_platform"] = hosting_platform

    RunTest(
        copie,
        configuration,
        snapshot,
        include_globs={filename},
    )

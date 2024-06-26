import re

from datetime import datetime

import pytest

from TestHelpers import *


# ----------------------------------------------------------------------
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
        include_files={"LICENSE.txt"},
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

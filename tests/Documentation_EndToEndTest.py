import re

from datetime import datetime
from typing import Match

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
def test_License(license, copie, snapshot):
    configuration_info = next(
        ci for ci in ConfigurationInfo.Generate() if ci.configuration["generate_docs"]
    )

    configuration_info.configuration["documentation_license"] = license

    project_dir = RunTest(copie, configuration_info.configuration)
    assert project_dir is not None

    license_filename = project_dir / "LICENSE.txt"

    if license == "None":
        assert not license_filename.is_file(), license_filename
        return

    license_content = license_filename.read_text(encoding="utf-8")

    copyright_found = False

    # ----------------------------------------------------------------------
    def Sub(
        match: Match,
    ) -> str:
        nonlocal copyright_found
        copyright_found = True

        return "<Scrubbed copyright>"

    # ----------------------------------------------------------------------

    license_content = re.sub(
        rf"""(?#
        Beginning of line   )^(?#
        Copyright           )Copyright\s+(?#
        Mark                )(?:\([cC]\)\s+)?(?#
        Year                ){datetime.now().year}\s+(?#
        Project Name        ){configuration_info.configuration['author_name']}(?#
        End of line         )$(?#
        )""",
        Sub,
        license_content,
        flags=re.MULTILINE,
    )

    assert copyright_found, license_content
    assert license_content == snapshot

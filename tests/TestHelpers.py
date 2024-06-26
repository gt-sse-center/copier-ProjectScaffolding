import os
import uuid

from pathlib import Path
from typing import Any

import pytest


# ----------------------------------------------------------------------
@pytest.fixture
def configuration() -> dict[str, Any]:
    create_unique_string_func = lambda: str(uuid.uuid4()).lower().replace("-", "")

    return {
        "project_name": create_unique_string_func(),
        "project_description": create_unique_string_func(),
        "author_name": create_unique_string_func(),
        "author_email": f"{create_unique_string_func()}@example.com",
        "generate_docs": True,
        "documentation_license": "MIT",
    }


# ----------------------------------------------------------------------
def RunTest(
    copie: Any,
    configuration: dict[str, Any],
    snapshot: Any,
    include_files: set[str] | None = None,
    exclude_files: set[str] | None = None,
) -> dict[str, str | None]:
    result = copie.copy(extra_answers=configuration)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir.is_dir(), result.project_dir

    output = ParseOutput(
        configuration,
        result.project_dir,
        include_files or set(),
        exclude_files or set(),
    )
    assert output == snapshot

    return output


# ----------------------------------------------------------------------
def ParseOutput(
    configuration: dict[str, Any],
    output_dir: Path,
    include_files: set[str],
    exclude_files: set[str],
) -> dict[str, str | None]:
    results: dict[str, str | None] = {}

    for root_str, _, filenames in os.walk(output_dir):
        root = Path(root_str)
        relative_path = root.relative_to(output_dir)

        if not filenames:
            results[relative_path.as_posix()] = None
        else:
            for filename in filenames:
                if filename == ".copier-answers.yml":
                    continue

                key = (relative_path / filename).as_posix()

                if key in exclude_files:
                    continue
                if include_files and key not in include_files:
                    continue

                content = (root / filename).read_text(encoding="utf-8")

                for attribute in [
                    "project_name",
                    "project_description",
                    "author_name",
                    "author_email",
                ]:
                    content = content.replace(configuration[attribute], f"<<{attribute}>>")

                results[key] = content

    return results

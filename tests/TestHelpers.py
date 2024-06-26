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
        "hosting_platform": "GitHub",
        "github_username": create_unique_string_func(),
        "github_repo_name": create_unique_string_func(),
    }


# ----------------------------------------------------------------------
def RunTest(
    copie: Any,
    configuration: dict[str, Any],
    snapshot: Any,
    include_globs: set[str] | None = None,
    exclude_globs: set[str] | None = None,
) -> dict[str, str | None]:
    result = copie.copy(extra_answers=configuration)

    assert result.exit_code == 0, result
    assert result.exception is None
    assert result.project_dir.is_dir(), result.project_dir

    output = ParseOutput(
        configuration,
        result.project_dir,
        include_globs or set(),
        exclude_globs or set(),
    )
    assert output == snapshot

    return output


# ----------------------------------------------------------------------
def ParseOutput(
    configuration: dict[str, Any],
    output_dir: Path,
    include_globs: set[str],
    exclude_globs: set[str],
) -> dict[str, str | None]:
    results: dict[str, str | None] = {}

    include_files: set[str] = set()
    exclude_files: set[str] = set()

    for include_glob in include_globs:
        include_files.update(set(result.as_posix() for result in output_dir.rglob(include_glob)))
    for exclude_glob in exclude_globs:
        exclude_files.update(set(result.as_posix() for result in output_dir.rglob(exclude_glob)))

    for root_str, _, filenames in os.walk(output_dir):
        root = Path(root_str)
        relative_path = root.relative_to(output_dir)

        if not filenames:
            results[relative_path.as_posix()] = None
        else:
            for filename in filenames:
                if filename == ".copier-answers.yml":
                    continue

                fullpath = root / filename
                fullpath_str = fullpath.as_posix()

                if fullpath_str in exclude_files:
                    continue

                # Note that in the following comparison, we are looking at the input globs rather
                # than the files produced by the globs. This is because the globs may refer to a
                # directory (where the length will be 1) where as there may not be any files
                # within that directory (where the length will be 0).
                if include_globs and fullpath_str not in include_files:
                    continue

                content = fullpath.read_text(encoding="utf-8")

                for attribute in [
                    "project_name",
                    "project_description",
                    "author_name",
                    "author_email",
                ]:
                    content = content.replace(configuration[attribute], f"<<{attribute}>>")

                results[(relative_path / filename).as_posix()] = content

    return results

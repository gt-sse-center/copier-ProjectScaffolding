import uuid

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generator


# ----------------------------------------------------------------------
freeform_strings: list[str] = [
    "project_description",
    "author_name",
    "author_email",
    "github_username",
    "github_repo_name",
]


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ConfigurationInfo:
    # ----------------------------------------------------------------------
    name: str
    configuration: dict[str, Any]
    is_valid: bool = field(kw_only=True)

    # ----------------------------------------------------------------------
    @classmethod
    def Generate(
        cls,
        *,
        include_invalid: bool = False,
    ) -> Generator["ConfigurationInfo", None, None]:
        configuration: dict[str, Any] = {
            "_git_disable_directory_check": True,
            "_git_suppress_permission_instructions": True,
        }

        for freeform_string in freeform_strings:
            configuration[freeform_string] = str(uuid.uuid4()).lower().replace("-", "")

        # Do not make the project name random, as it needs to remain consistent across invocations
        # for valid comparisons.
        configuration["project_name"] = "this_is_the_project_name"

        # Ensure that the email address is valid
        configuration["author_email"] = f"{configuration['author_email']}@example.com"

        configuration_ctr = 0

        for generate_docs in [False, True]:
            configuration["generate_docs"] = generate_docs

            for repository_tool in ["None", "git"]:
                configuration["repository_tool"] = repository_tool

                for hosting_platform in ["None", "GitHub"]:
                    if hosting_platform == "GitHub" and repository_tool != "git":
                        is_valid = False
                    else:
                        is_valid = True

                    if not include_invalid and not is_valid:
                        continue

                    configuration["hosting_platform"] = hosting_platform

                    for project_type in ["None", "PythonExecutionEnvironment", "PythonPackage"]:
                        configuration["project_type"] = project_type

                        configuration_ctr += 1

                        yield cls(
                            f"{configuration_ctr:02}-{generate_docs}_{repository_tool}_{hosting_platform}_{project_type}",
                            configuration,
                            is_valid=is_valid,
                        )


# ----------------------------------------------------------------------
def RunTest(
    copie: Any,
    configuration: dict[str, Any],
    expect_failure: bool = False,
) -> Path | None:
    result = copie.copy(extra_answers=configuration)

    if expect_failure:
        assert result.exit_code != 0, result.exit_code
        assert result.exception is not None
        return None

    assert result.exit_code == 0, result
    assert result.exception is None
    assert result.project_dir.is_dir(), result.project_dir

    return result.project_dir

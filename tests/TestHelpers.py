import uuid

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generator

from dbrownell_Common.ContextlibEx import ExitStack


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

        configuration_name_parts: list[str] = []
        configuration_ctr = 0
        is_valid = False

        # ----------------------------------------------------------------------
        def CreateConfigurationInfo(
            configuration: dict[str, Any],
        ) -> ConfigurationInfo:
            nonlocal configuration_ctr

            configuration_ctr += 1
            configuration_name = f"{configuration_ctr:02}_{'_'.join(configuration_name_parts)}"

            return ConfigurationInfo(
                configuration_name,
                configuration,
                is_valid=is_valid,
            )

        # ----------------------------------------------------------------------
        def DeleteConfigurationValue(
            key: str,
        ) -> None:
            del configuration[key]

        # ----------------------------------------------------------------------

        configuration_name_parts.append("<placeholder>")
        with ExitStack(configuration_name_parts.pop):
            for generate_docs in [False, True]:
                configuration["generate_docs"] = generate_docs
                configuration_name_parts[-1] = f"Docs{int(generate_docs)}"

                configuration_name_parts.append("<placeholder>")
                with ExitStack(configuration_name_parts.pop):
                    for repository_tool in ["None", "git"]:
                        configuration["repository_tool"] = repository_tool
                        configuration_name_parts[-1] = repository_tool

                        configuration_name_parts.append("<placeholder>")
                        with ExitStack(configuration_name_parts.pop):
                            for hosting_platform in ["None", "GitHub"]:
                                if hosting_platform == "GitHub" and repository_tool != "git":
                                    is_valid = False
                                else:
                                    is_valid = True

                                if not include_invalid and not is_valid:
                                    continue

                                configuration["hosting_platform"] = hosting_platform
                                configuration_name_parts[-1] = hosting_platform

                                configuration_name_parts.append("<placeholder>")
                                with ExitStack(configuration_name_parts.pop):
                                    for project_type in [
                                        "None",
                                        "PythonExecutionEnvironment",
                                        "PythonPackage",
                                    ]:
                                        configuration["project_type"] = project_type
                                        configuration_name_parts[-1] = project_type

                                        if (
                                            project_type != "PythonPackage"
                                            or hosting_platform != "GitHub"
                                        ):
                                            yield CreateConfigurationInfo(configuration)
                                            continue

                                        configuration_name_parts.append("<placeholder>")
                                        with ExitStack(
                                            configuration_name_parts.pop,
                                            lambda key="python_package_generate_ci": DeleteConfigurationValue(
                                                key
                                            ),
                                        ):
                                            for generate_ci in [False, True]:
                                                configuration["python_package_generate_ci"] = (
                                                    generate_ci
                                                )
                                                configuration_name_parts[-1] = (
                                                    f"CI{int(generate_ci)}"
                                                )

                                                if not generate_ci:
                                                    yield CreateConfigurationInfo(configuration)
                                                    continue

                                                configuration_name_parts.append("<placeholder>")
                                                with ExitStack(
                                                    configuration_name_parts.pop,
                                                    lambda key="python_package_generate_ci_binary_question": DeleteConfigurationValue(
                                                        key
                                                    ),
                                                ):
                                                    for generate_binary in [False, True]:
                                                        configuration[
                                                            "python_package_generate_ci_binary_question"
                                                        ] = generate_binary
                                                        configuration_name_parts[-1] = (
                                                            f"CIBinary{int(generate_binary)}"
                                                        )

                                                        yield CreateConfigurationInfo(configuration)


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

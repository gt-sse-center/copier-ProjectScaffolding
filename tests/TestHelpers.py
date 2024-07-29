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
        yield from _ConfigurationGenerator().Enumerate(include_invalid=include_invalid)


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


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
class _ConfigurationGenerator:
    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        configuration: dict[str, Any] = {
            "_python_package_generate_ci_persist_coverage_simulate_gist_id": True,
            "_python_package_generate_ci_simulate_openssf_id": True,
            "_python_package_generate_ci_sign_artifacts_simulate_keygen": True,
        }

        for freeform_string in freeform_strings:
            configuration[freeform_string] = str(uuid.uuid4()).lower().replace("-", "")

        # Do not make the project name random, as it needs to remain consistent across invocations
        # for valid comparisons (for example, when the name is used to create directories).
        configuration["project_name"] = "this_is_the_project_name"

        # Ensure that the email address is valid
        configuration["author_email"] = f"{configuration['author_email']}@example.com"

        # Commit the values
        self.configuration_name_parts: list[str] = []
        self.configuration = configuration
        self._configuration_ctr = 0

    # ----------------------------------------------------------------------
    def Enumerate(
        self,
        include_invalid: bool = False,
    ) -> Generator[ConfigurationInfo, None, None]:
        self._configuration_ctr = 1

        for _ in self._EnumerateValues("generate_docs", "Docs{}", [False, True]):
            for _ in self._EnumerateValues("repository_tool", "{}", ["None", "git"]):
                for _ in self._EnumerateValues("hosting_platform", "{}", ["None", "GitHub"]):
                    if (
                        self.configuration["hosting_platform"] == "GitHub"
                        and self.configuration["repository_tool"] != "git"
                    ):
                        is_valid = False
                    else:
                        is_valid = True

                    if not include_invalid and not is_valid:
                        continue

                    for _ in self._EnumerateValues(
                        "project_type",
                        "{}",
                        [
                            "None",
                            "PythonExecutionEnvironment",
                            "PythonPackage",
                        ],
                    ):
                        if (
                            self.configuration["project_type"] != "PythonPackage"
                            or self.configuration["hosting_platform"] != "GitHub"
                        ):
                            yield self._CreateConfigurationInfo(is_valid)
                            continue

                        for _ in self._EnumerateValues(
                            "python_package_generate_ci", "CI{}", [False, True]
                        ):
                            if not self.configuration["python_package_generate_ci"]:
                                yield self._CreateConfigurationInfo(is_valid)
                                continue

                            for _ in self._EnumerateValues(
                                "python_package_generate_ci_persist_coverage_question",
                                "Coverage{}",
                                [False, True],
                            ):
                                for _ in self._EnumerateValues(
                                    "python_package_generate_ci_openssf_question",
                                    "OpenSSF{}",
                                    [False, True],
                                ):
                                    if (
                                        not self.configuration["generate_docs"]
                                        and self.configuration[
                                            "python_package_generate_ci_openssf_question"
                                        ]
                                    ):
                                        continue

                                    for _ in self._EnumerateValues(
                                        "python_package_generate_ci_binary_question",
                                        "Binary{}",
                                        [False, True],
                                    ):
                                        for _ in self._EnumerateValues(
                                            "python_package_generate_ci_docker_image_question",
                                            "DockerImage{}",
                                            [False, True],
                                        ):
                                            for _ in self._EnumerateValues(
                                                "python_package_generate_ci_sign_artifacts_question",
                                                "Sign{}",
                                                [False, True],
                                            ):
                                                yield self._CreateConfigurationInfo(is_valid)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def _DeleteConfigurationValue(
        self,
        key: str,
    ) -> None:
        del self.configuration[key]

    # ----------------------------------------------------------------------
    def _EnumerateValues(
        self,
        configuration_key: str,
        name_key_template: str,
        values: list[Any],
    ) -> Generator[dict[str, Any], None, None]:
        self.configuration_name_parts.append("<placeholder>")
        with ExitStack(
            self.configuration_name_parts.pop,
            lambda key=configuration_key: self._DeleteConfigurationValue(key),
        ):
            for value in values:
                self.configuration[configuration_key] = value

                name_value = value

                if isinstance(value, bool):
                    name_value = int(name_value)

                self.configuration_name_parts[-1] = name_key_template.format(name_value)

                yield self.configuration

    # ----------------------------------------------------------------------
    def _CreateConfigurationInfo(
        self,
        is_valid: bool,
    ) -> ConfigurationInfo:
        configuration_name = (
            f"{self._configuration_ctr:02}_{'_'.join(self.configuration_name_parts)}"
        )
        self._configuration_ctr += 1

        return ConfigurationInfo(
            configuration_name,
            self.configuration,
            is_valid=is_valid,
        )

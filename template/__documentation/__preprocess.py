import sys
import shutil
import textwrap

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
def MoveContent():
    output_dir = EnsureDir(Path.cwd())
    documentation_dir = EnsureDir(output_dir / "__documentation")
    licenses_dir = EnsureDir(documentation_dir / "__licenses")

    if "{{ documentation_license }}" != "None":
        MoveFile(
            EnsureFile(licenses_dir / "{{ documentation_license }}_LICENSE.txt"),
            documentation_dir,
            "LICENSE.txt",
        )

    shutil.rmtree(licenses_dir)

    MoveFiles(documentation_dir, output_dir)


# ----------------------------------------------------------------------
def UpdateContributingFile():
    replacement_info: dict[str, str] = {}

    if "{{ hosting_platform }}" == "None":
        replacement_info["General Information"] = "TODO: Include information on how to submit pull requests and/or issues.\n"
        replacement_info["Pull Requests and Branches"] = "TODO: Include information on how to use branches effectively and create a pull request.\n"
        replacement_info["Proposals"] = "TODO: Include information on how proposals are handled.\n"
    elif "{{ hosting_platform }}" == "GitHub":
        replacement_info["General Information"] = "For specific proposals, please provide them as [pull requests](https://github.com/coreinfrastructure/best-practices-badge/pulls) or [issues](https://github.com/coreinfrastructure/best-practices-badge/issues) via our [GitHub site]({{ github_url }}).\n"
        replacement_info["Pull Requests and Branches"] = textwrap.dedent(
            """\
            Pull requests are preferred, since they are specific. For more about how to create a pull request, see https://help.github.com/articles/using-pull-requests/.

            We recommend creating different branches for different (logical) changes, and creating a pull request into the `main` branch when you're done. See the GitHub documentation on [creating branches](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/) and [using pull requests](https://help.github.com/articles/using-pull-requests/).
            """,
        )
        replacement_info["Proposals"] = "We use GitHub to track proposed changes via its [issue tracker](https://github.com/coreinfrastructure/best-practices-badge/issues) and [pull requests](https://github.com/coreinfrastructure/best-practices-badge/pulls). Specific changes are proposed using those mechanisms. Issues are assigned to an individual, who works and then marks it complete. If there are questions or objections, the conversation of that issue or pull request is used to resolve it.\n"
    else:
        raise Exception("'{{ hosting_platform }}' is not a recognized hosting platform.")

    _UpdateFile(Path.cwd() / "CONTRIBUTING.md", replacement_info)


# ----------------------------------------------------------------------
def UpdateDevelopmentFile():
    replacement_info: dict[str, str] = {}

    if "{{ project_type }}" == "None":
        replacement_info["Development Activities"] = "TODO: Complete this section\n"
        replacement_info["Enlistment"] = "TODO: Complete this section\n"
    else:
        enlistment_steps: list[str] = []

        if "{{ hosting_platform }}" == "None":
            pass # Nothing to do here
        elif "{{ hosting_platform }}" == "GitHub":
            enlistment_steps.append(
                textwrap.dedent(
                    """\
                    <tr>
                        <td>1. Clone the repository locally</td>
                        <td><code>git clone {{ github_url }}</code></td>
                        <td><a href="https://git-scm.com/docs/git-clone" target="_blank">https://git-scm.com/docs/git-clone</a></td>
                    </tr>
                    """,
                ),
            )
        else:
            raise Exception("'{{ hosting_platform }}' is not a recognized hosting platform.")

        if "{{ project_type }}" in ["PythonExecutionEnvironment", "PythonPackage"]:
            # Development Activities
            if "{{ project_type }}" == "PythonExecutionEnvironment":
                replacement_info["Development Activities"] = "TODO: Complete this section\n"
            elif "{{ project_type }}" == "PythonPackage":
                replacement_info["Development Activities"] = textwrap.dedent(
                    """\
                    Each of these activities can be invoked from an activated terminal on your local machine.

                    | Activity | Command Line | Description | Invoked by Continuous Integration |
                    | --- | --- | --- | --- |
                    | Code Formatting | `python Build.py black [--format]` | Format source code using [black](https://github.com/psf/black) based on settings in `pyproject.toml`. | |
                    | Static Code Analysis | `python Build.py pylint` | Validate source code using [pylint](https://github.com/pylint-dev/pylint) based on settings in `pyproject.toml`. | |
                    | Automated Testing | `python Build.py pytest [--code-coverage]` | Run automated tests using [pytest](https://docs.pytest.org/) and (optionally) extract code coverage information using [coverage](https://coverage.readthedocs.io/) based on settings in `pyproject.toml`. | |
                    | Semantic Version Generation | `python Build.py update_version` | Generate a new [Semantic Version](https://semver.org) based on git commits using [AutoGitSemVer](https://github.com/davidbrownell/AutoGitSemVer). Version information is stored in `/src/{{ python_package_pypi_name }}/__init__.py`. | |
                    | Python Package Creation | <p><code>python Build.py package</code></p><p>Requires that the repository was bootstrapped with the <code>--package</code> flag. | Create a python package using [setuptools](https://github.com/pypa/setuptools) based on settings in `pyproject.toml`. | |
                    | Python Package Publishing | <p><code>python Build.py publish</code></p><p>Requires that the repository was bootstrapped with the <code>--package</code> flag. | Publish a python package to [PyPi](https://pypi.org). | |
                    | Build Binaries | `python Build.py build_binaries` |  Create a python binary for your current operating system using [cx_Freeze](https://cx-freeze.readthedocs.io/) based on settings in `src/BuildBinary.py`. | |
                    | Development Docker Image | `python Build.py create_docker_image` | Create a [docker](https://docker.com) image for a bootstrapped development environment. This functionality is useful when adhering to the [FAIR principles for research software](https://doi.org/10.1038/s41597-022-01710-x) by supporting the creation of a development environment and its dependencies as they existed at the moment when the image was created. | |
                    """,
                )
            else:
                raise Exception("'{{ project_type }}' is not a recognized project type.")

            # Enlistment
            step_offset = len(enlistment_steps)

            enlistment_steps += [
                textwrap.dedent(
                    f"""\
                    <tr>
                        <td>{step_offset + 1}. Bootstrap the environment</td>
                        <td>
                            <table>
                                <tr>
                                    <th>Linux / MacOS</th>
                                    <td><code>./Bootstrap.sh [--python-version &lt;python version&gt;]</code></td>
                                </tr>
                                <tr>
                                    <th>Windows</th>
                                    <td><code>Bootstrap.cmd [--python-version &lt;python version&gt;]</code></td>
                                </tr>
                            </table>
                        </td>
                        <td>Prepares the repository for local development by enlisting in all dependencies.</td>
                    </tr>
                    """,
                ),
                textwrap.dedent(
                    f"""\
                    <tr>
                        <td>{step_offset + 2}. Activate the environment</td>
                        <td>
                            <table>
                                <tr>
                                    <th>Linux / MacOS</th>
                                    <td><code>. ./Activate.sh</code></td>
                                </tr>
                                <tr>
                                    <th>Windows</th>
                                    <td><code>Activate.cmd</code></td>
                                </tr>
                            </table>
                        </td>
                        <td>
                            <p>Activates the terminal for development. Each new terminal window must be activated.</p>
                            <p>Activate.sh/.cmd is actually a shortcut to the most recently bootstrapped version of python (e.g. Activate3.11.sh/.cmd). With this functionality, it is possible to support multiple python versions in the same repository and activate each in a terminal using the python-specific activation script.</p>
                        </td>
                    </tr>
                    """,
                ),
                textwrap.dedent(
                    f"""\
                    <tr>
                        <td>{step_offset + 3}. [Optional] Deactivate the environment</td>
                        <td>
                            <table>
                                <tr>
                                    <th>Linux / MacOS</th>
                                    <td><code>. ./Deactivate.sh</code></td>
                                </tr>
                                <tr>
                                    <th>Windows</th>
                                    <td><code>Deactivate.cmd</code></td>
                                </tr>
                            </table>
                        </td>
                        <td>
                            Deactivates the terminal environment. Deactivating is optional, as the terminal window itself may be closed when development activities are complete.
                        </td>
                    </tr>
                    """,
                ),
            ]

        else:
            raise Exception("'{{ project_type }}' is not a recognized project type.")

        replacement_info["Enlistment"] = textwrap.dedent(
            """\
            Enlistment in this repository involves these steps.

            <table>
            <tr>
                <th>Step</th>
                <th>Command Line</th>
                <th>Description</th>
            </tr>
            {}
            </table>
            """,
        ).format(''.join(enlistment_steps).rstrip())

    _UpdateFile(Path.cwd() / "DEVELOPMENT.md", replacement_info)


# ----------------------------------------------------------------------
def UpdateReadmeFile():
    replacement_info: dict[str, str] = {}

    if "{{ project_type }}" == "None":
        replacement_info["Badges"] = ""
        replacement_info["Installation"] = "TODO: Complete this section\n"
    elif "{{ project_type }}" == "PythonExecutionEnvironment":
        replacement_info["Badges"] = ""
        replacement_info["Installation"] = "No additional setup is required to use this project.\n"
    elif "{{ project_type }}" == "PythonPackage":
        replacement_info["Badges"] = "" # TODO

        pip_instructions = textwrap.dedent(
            """\
            ### Installation via pip
            To install the {{ project_name }} package via [pip](https://pip.pypa.io/en/stable/) (Python Installer for Python) for use with your python code:

            `pip install {{ python_package_pypi_name }}`
            """,
        )

        if "{{ hosting_platform }}" == "None":
            installation_instructions = pip_instructions
        elif "{{ hosting_platform }}" == "GitHub":
            installation_instructions = textwrap.dedent(
                """\
                {{ project_name }} can be installed via one of these methods:

                - [Installation via Executable](#installation-via-executable)
                - [Installation via pip](#installation-via-pip)

                ### Installation via Executable
                Download an executable for Linux, MacOS, or Windows to the the functionality provided by this repository without a dependency on python.

                1. Download the archive for the latest release [here]({{ github_url }}/releases/latest). The filename will begin with `exe.` and contain the name of your operating system.
                2. Decompress the archive.

                {}
                """,
            ).format(pip_instructions)
        else:
            raise Exception("'{{ hosting_platform }}' is not a recognized hosting platform.")

        replacement_info["Installation"] = installation_instructions

    else:
        raise Exception("'{{ project_type }}' is not a recognized project type.")

    _UpdateFile(Path.cwd() / "README.md", replacement_info)


# ----------------------------------------------------------------------
def UpdateSecurityFile():
    replacement_info: dict[str, str] = {}

    if "{{ hosting_platform }}" == "None":
        replacement_info["Submit Vulnerability"] = "TODO: Include information on how to securely submit a vulnerability.\n"
    elif "{{ hosting_platform }}" == "GitHub":
        replacement_info["Submit Vulnerability"] = textwrap.dedent(
            '''\
            We prefer that you use the [GitHub mechanism for privately reporting a vulnerability](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability#privately-reporting-a-security-vulnerability). Under the [main repository's security tab]({{ github_url }}/security), in the left sidebar, under "Reporting", click "Advisories", click the "New draft security advisory" button to open the advisory form.
            [issues](https://github.com/coreinfrastructure/best-practices-badge/issues) via our [GitHub site]({{ github_url }}).
            ''',
        )
    else:
        raise Exception("'{{ hosting_platform }}' is not a recognized hosting platform.")

    _UpdateFile(Path.cwd() / "SECURITY.md", replacement_info)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _UpdateFile(
    filename: Path,
    replacement_info: dict[str, str],
) -> None:
    EnsureFile(filename)

    content = filename.read_text(encoding="utf-8")

    for tag_name, new_content in replacement_info.items():
        content = ReplaceContent(
            filename.suffix,
            tag_name,
            content,
            new_content,
        )

    filename.write_text(content, encoding="utf-8")


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    {% if generate_docs %}
    MoveContent()

    UpdateContributingFile()
    UpdateDevelopmentFile()
    UpdateReadmeFile()
    UpdateSecurityFile()
    {% else %}
    pass
    {% endif %}

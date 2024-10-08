import os
import stat
import sys
import textwrap

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
def MoveContent():
    output_dir = EnsureDir(Path.cwd())
    post_generation_actions_dir = EnsureDir(output_dir / "__post_generation_actions")

    MoveFiles(post_generation_actions_dir, output_dir)


# ----------------------------------------------------------------------
def UpdatePostGenerationActionsFile():
    instructions: dict[str, str] = {}

    _CreateGitHubSettings(instructions)
    _CreatePrePythonPackageCIInstructions(instructions)
    _CreatePreMinisignInstructions(instructions)

    # Commit instructions
    _CreateCommitInstructions(instructions)

    _CreatePostPythonPackageCIInstructions(instructions)
    _CreatePostProjectSpecificCIInstructions(instructions)
    _CreatePostDocumentationInstructions(instructions)
    _CreateOpenSSFBadgeInstructions(instructions)
    _CreatePostFinalInstructions(instructions)

    UpdateFile(
        Path() / "post_generation_actions.html",
        {
            "Instructions": "\n".join(
                textwrap.dedent(
                    """\
                    <details>
                        <summary>
                            <span role="term"><input type="checkbox" id="{title_id}">{index}) {title}</span>
                        </summary>
                    </details>
                    <div role="definition" class="details-content">
                        {steps_html}
                    </div>
                    """
                ).format(
                    index=index + 1,
                    title_id=title.lower().replace(' ', '-'),
                    title=title,
                    steps_html=instruction,
                )
                for index, (title, instruction) in enumerate(instructions.items())
            ),
        },
    )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _CreateCommitInstructions(
    instructions: dict[str, str],
) -> None:
    shell_scripts: list[Path] = []

    if "{{ project_type }}" == "None":
        pass # Nothing to do here
    elif "{{ project_type }}" in ["PythonExecutionEnvironment", "PythonPackage"]:
        shell_scripts.append(Path.cwd() / "Bootstrap.sh")
    else:
        raise Exception("'{{ project_type }}' is not a recognized project type.")

    if "{{ repository_tool }}" == "None":
        pass # Nothing to do here
    elif "{{ repository_tool }}" == "git":
        # The Windows file system does not recognize Linux/MacOS file permissions. Therefore, we need
        # to ensure that the permissions are set correctly within git so that the repository can be
        # used correctly on those systems.
        precommit_permissions = ""
        commit_step_num = 2
        push_step_num = 3

        if shell_scripts:
            for shell_script in shell_scripts:
                shell_script.chmod(
                    shell_script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
                )

            # Note that these precommit permissions are only necessary when running on Windows, but
            # detecting if we are on Windows turns out to be tricky. For example, we are technically
            # "running on Windows" when a docker container is run on a Windows host, where the
            # container generates output to a volume mounted from the host. Always output the
            # instructions, just to be on the safe side.
            precommit_permissions = "{}<br/>\n".format("<br/>\n".join(f'{commit_step_num + index}. <code>git update-index --chmod=+x "{script.relative_to(Path.cwd())}"</code>' for index, script in enumerate(shell_scripts)))

            commit_step_num += len(shell_scripts)
            push_step_num += len(shell_scripts)

        instructions["Initialize the git repository"] = textwrap.dedent(
            """\
            <p>In this step, we will commit the files generated in git and push the changes.</p>

            <p>Open a terminal window, navigate to your repository, and run the following commands:</p>

            1. <code>git add --all</code><br/>
            {precommit_permissions}{commit_step_num}. <code>git commit -m "🎉 Initial commit"</code><br/>
            {push_step_num}. <code>git push</code><br/>
            </p>
            """,
        ).format(
            precommit_permissions=precommit_permissions,
            commit_step_num=commit_step_num,
            push_step_num=push_step_num,
        )
    else:
        raise Exception("'{{ repository_tool }}' is not a recognized repository tool.")


# ----------------------------------------------------------------------
def _CreateGitHubSettings(
    instructions: dict[str, str],
) -> None:
    if "{{ hosting_platform }}" != "GitHub":
        return

    instructions["Update GitHub Settings"] = textwrap.dedent(
        """\
        <p>In this step, we will update GitHub settings to allow the creation of git tags during a release.</p>
        <ol>
          <li>Visit <a href="{{ github_url }}/settings/actions" target="_blank">{{ github_url }}/settings/actions</a>.</li>
          <li>In the "Workflow permissions" section...</li>
          <li>Select "Read and write permissions".</li>
          <li>Click the "Save" button.</li>
        </ol>
        """,
    )


# ----------------------------------------------------------------------
def _CreatePrePythonPackageCIInstructions(
    instructions: dict[str, str],
) -> None:
    if "{{ python_package_generate_ci }}".lower() != "true":
        return

    # Create and save the temporary PyPi token
    instructions["Create a Temporary PyPi Token"] = textwrap.dedent(
        """\
        <p>In this step, we will create a temporary <a href="https://pypi.org" target="_blank">PyPi</a> token used to publish the python package for the first time. The token created will be scoped to all of your projects on PyPi (which provides too much access). Once the package has been published for the first time, we will delete this temporary token and create a new one that is scoped to the single project.</p>
        <ol>
          <li>Visit <a href="https://pypi.org/manage/account/token/" target="_blank">https://pypi.org/manage/account/token/</a>.</li>
          <li>
            <p>Enter the values:</p>
            <p>
              <table>
                <tr>
                  <th>Token name:</th>
                  <td><code>Temporary CI Publish Action ({{ python_package_pypi_name }})</code></td>
                </tr>
                <tr>
                  <th>Scope:</th>
                  <td><code>Entire account (all projects)</code></td>
                </tr>
              </table>
            </p>
          </li>
          <li>Click the "Create token" button.</li>
          <li>Click the "Copy token" button for use in the next step.</li>
        </ol>
        """,
    )

    if "{{ hosting_platform }}" == "None":
        instructions["Save the Temporary PyPi Token"] = textwrap.dedent(
            """\
            <p>Please save the PyPi token just created.</p>
            """,
        )
    elif "{{ hosting_platform }}" == "GitHub":
        instructions["Save the Temporary PyPi Token as a GitHub Secret"] = textwrap.dedent(
            """\
            <p>In this step, we will save the PyPi token just created as a <a href="https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions" target="_blank">GitHub Action secret</a>.</p>
            <ol>
              <li>Visit <a href="{{ github_url }}/settings/secrets/actions/new" target="_blank">{{ github_url }}/settings/secrets/actions/new</a>.</li>
              <li>
                <p>Enter the values:</p>
                <p>
                  <table>
                    <tr>
                      <th>Name:</th>
                      <td><code>PYPI_TOKEN</code></td>
                    </tr>
                    <tr>
                      <th>Secret:</th>
                      <td>&lt;paste the token generated in the previous step&gt;</td>
                    </tr>
                  </table>
                </p>
              </li>
              <li>Click the "Add secret" button.</li>
            </ol>
            """,
        )

        if "{{ python_package_generate_ci_persist_coverage }}".lower() == "true":
            instructions["Create a GitHub Personal Access Token for gists"] = textwrap.dedent(
                """\
                <p>In this step, we will create a GitHub Personal Access Token (PAT) used when persisting code coverage information between Continuous Integration runs.</p>
                <ol>
                  <li>Visit <a href="{{ github_host }}/settings/tokens?type=beta" target="_blank">{{ github_host }}/settings/tokens?type=beta</a>.</li>
                  <li>Click the "Generate new token" button.</li>
                  <li>Name the token <code>GitHub Workflow Gist ({{ github_repo_name }})</code>.</li>
                  <li>In the Repository access section...</li>
                  <li>Select "Only select repositories"...</li>
                  <li>Select <code>{{ github_repo_name }}</code>.</li>
                  <li>In the "Permissions" section...</li>
                  <li>Press the "Account permissions" dropdown...</li>
                  <li>Select the "Gists" section...</li>
                  <li>Click the "Access: No access" dropdown button...</li>
                  <li>Select "Read and write".</li>
                  <li>Click the "Generate token" button.</li>
                  <li>Copy the token for use in the next step.</li>
                </ol>
                """,
            )

            instructions["Save the GitHub Personal Access Token for gists"] = textwrap.dedent(
                """\
                <p>In this step, we will save the GitHub Personal Access Token just created as a <a href="https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions" target="_blank">GitHub Action secret</a>.</p>
                <ol>
                  <li>Visit <a href="{{ github_url }}/settings/secrets/actions/new" target="_blank">{{ github_url }}/settings/secrets/actions/new</a>.</li>
                  <li>
                    <p>Enter the values:</p>
                    <p>
                      <table>
                        <tr>
                          <th>Name:</th>
                          <td><code>GIST_TOKEN</code></td>
                        </tr>
                        <tr>
                          <th>Secret:</th>
                          <td>&lt;paste the token generated in the previous step&gt;</td>
                        </tr>
                      </table>
                    </p>
                  </li>
                  <li>Click the "Add secret" button.</li>
                </ol>
                """,
            )
    else:
        raise Exception("'{{ hosting_platform }}' is not a recognized hosting platform.")


# ----------------------------------------------------------------------
def _CreatePreMinisignInstructions(
    instructions: dict[str, str],
) -> None:
    if "{{ python_package_generate_ci_sign_artifacts }}".lower() != "true":
        return

    # Create instructions to create the secret
    if "{{ hosting_platform }}" == "None":
        instructions["Save the Minisign Private Key"] = "<p>Please save the PyPi token just created.</p>"
    elif "{{ hosting_platform }}" == "GitHub":
        instructions["Save the Minisign Private Key"] = textwrap.dedent(
            """\
            <p>In this step, we will save the Minisign private key just created as a <a href="https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions" target="_blank">GitHub Action secret</a>.</p>
            <ol>
              <li>Open `minisign_key.pri` in a text editor and copy the contents.</li>
              <li>Visit <a href="{{ github_url }}/settings/secrets/actions/new" target="_blank">{{ github_url }}/settings/secrets/actions/new</a>.</li>
              <li>
                <p>Enter the values:</p>
                <p>
                  <table>
                    <tr>
                      <th>Name:</th>
                      <td><code>MINISIGN_PRIVATE_KEY</code></td>
                    </tr>
                    <tr>
                      <th>Secret:</th>
                      <td>&lt;paste the private key previously copied&gt;</td>
                    </tr>
                  </table>
                </p>
              </li>
              <li>Click the "Add secret" button.</li>
            </ol>
            """,
        )
    else:
        raise Exception("'{{ hosting_platform }}' is not a recognized hosting platform.")

    # Create instructions to delete the private key
    instructions["Store the Minisign Private Key"] = textwrap.dedent(
        """\
        <p>Store the Minisign private key in a secure location. Once you have stored the key, you can delete it from your local machine.</p>
        <p>Note that you should NEVER force <code>minisign_key.pri</code> into source control.</p>
        """,
    )


# ----------------------------------------------------------------------
def _CreatePostPythonPackageCIInstructions(
    instructions: dict[str, str],
) -> None:
    if "{{ python_package_generate_ci }}".lower() != "true":
        return

    # Wait for the workflow to complete
    if "{{ hosting_platform }}" == "None":
        instructions["Verify the CI/CD Workflow"] = textwrap.dedent(
            """\
            <p>Please verify that the CI/CD workflow completed successfully.</p>
            """,
        )
    elif "{{ hosting_platform }}" == "GitHub":
        instructions["Verify the CI/CD Workflow"] = textwrap.dedent(
            """\
            <p>In this step, we will verify that the GitHub Action workflow completed successfully.</p>
            <ol>
              <li>Visit <a href="{{ github_url }}/actions" target="_blank">{{ github_url }}/actions</a>.</li>
              <li>Select the most recent workflow.</li>
              <li>Wait for the workflow to complete successfully.</li>
            </ol>
            """,
        )
    else:
        raise Exception("'{{ hosting_platform }}' is not a recognized hosting platform.")

    # Delete the temporary PyPi token, create an official PyPi token, and update the GitHub secret
    instructions["Delete the temporary PyPi Token"] = textwrap.dedent(
        """\
        <p>In an earlier step, we created a temporary <a href="https://pypi.org" target="_blank">PyPi</a> token. In this step, we will delete that token. A new token to replace it will be created in the steps that follow.</p>
        <ol>
          <li>Visit <a href="https://pypi.org/manage/account/" target="_blank">https://pypi.org/manage/account/</a>.</li>
          <li>Find the token named <code>Temporary CI Publish Action ({{ python_package_pypi_name }})</code>...</li>
          <li>Click the "Options" dropdown button...</li>
          <li>Select "Remove token".</li>
          <li>In the dialog box that appears...</li>
          <li>Enter your password.</li>
          <li>Click the "Remove API token" button.</li>
        </ol>
        """,
    )

    instructions["Create an Official PyPi Token"] = textwrap.dedent(
        """\
        <p>In this step, we create a new token scoped only to "{{ python_package_pypi_name }}".</p>

        <ol>
          <li>Visit <a href="https://pypi.org/manage/account/token/" target="_blank">https://pypi.org/manage/account/token/</a>.</li>
          <li>
            <p>Enter the values:</p>
            <p>
              <table>
                <tr>
                  <th>Token name:</th>
                  <td><code>CI Publish Action ({{ python_package_pypi_name }})</code></td>
                </tr>
                <tr>
                  <th>Scope:</th>
                  <td><code>Project: {{ python_package_pypi_name }}</code></td>
                </tr>
              </table>
            </p>
          </li>
          <li>Click the "Create token" button.</li>
          <li>Click the "Copy token" button for use in the next step.</li>
        </ol>
        """,
    )

    if "{{ hosting_platform }}" == "None":
        instructions["Save the PyPi Token"] = textwrap.dedent(
            """\
            <p>Please save the PyPi token just created.</p>
            """,
        )
    elif "{{ hosting_platform }}" == "GitHub":
        instructions["Update the GitHub Secret with the Official PyPi Token"] = textwrap.dedent(
            """\
            <p>In this step, we will save the PyPi token just created as a <a href="https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions" target="_blank">GitHub Action secret</a>.</p>
            <ol>
              <li>Visit <a href="{{ github_url }}/settings/secrets/actions/PYPI_TOKEN" target="_blank">{{ github_url }}/settings/secrets/actions/PYPI_TOKEN</a>.</li>
              <li>In the "Value" text window, paste the token generated in the previous step.</li>
              <li>Click "Update secret".</li>
            </ol>
            """,
        )
    else:
        raise Exception("'{{ hosting_platform }}' is not a recognized hosting platform.")


# ----------------------------------------------------------------------
def _CreatePostProjectSpecificCIInstructions(
    instructions: dict[str, str],
) -> None:
    if "{{ project_type }}" == "None":
        pass # Nothing to do here
    elif "{{ project_type }}" == "PythonExecutionEnvironment":
        instructions["Update requirements.txt"] = textwrap.dedent(
            """\
            <p>Python package dependencies can be added to <code>requirements.txt</code>. These packages will be automatically installed when the environment is <a href="https://github.com/davidbrownell/PythonBootstrapper" target="_blank">bootstrapped</a>.</p>
            <p>Please visit <a href="https://pip.pypa.io/en/stable/reference/requirements-file-format/" target="_blank">this link</a> for more information on requirements files and how they can be used.</p>
            """,
        )
    elif "{{ project_type }}" == "PythonPackage":
        instructions["Update pyproject.toml"] = textwrap.dedent(
            """\
            <p>Python development tools, package dependencies, and packaging instructions are configured in <code>pyproject.toml</code>. Please visit <a href="https://packaging.python.org/en/latest/guides/writing-pyproject-toml/" target="_blank">this link</a> for more information on these files.</p>
            <p>Please search for and replace all <code>TODO:</code> comments in <code>pyproject.toml</code>.</p>
            """,
        )
    else:
        raise Exception("'{{ project_type }}' is not a recognized project type.")


# ----------------------------------------------------------------------
def _CreatePostDocumentationInstructions(
    instructions: dict[str, str],
) -> None:
    if "{{ generate_docs }}".lower() == "true":
        filenames_to_update: list[str] = ["README.md", "MAINTAINERS.md"]

        if "{{ hosting_platform }}" == "None":
            filenames_to_update += ["CONTRIBUTING.md", "SECURITY.md"]
        elif "{{ hosting_platform }}" == "GitHub":
            pass # Noting to add here, as the content has already been populated
        else:
            raise Exception("'{{ hosting_platform }}' is not a recognized hosting platform.")

        if "{{ project_type }}" == "None":
            filenames_to_update.append("DEVELOPMENT.md")
        elif "{{ project_type }}" == "PythonExecutionEnvironment":
            filenames_to_update.append("DEVELOPMENT.md")
        elif "{{ project_type }}" == "PythonPackage":
            pass # Nothing to do here
        else:
            raise Exception("'{{ project_type }}' is not a recognized project type.")

        filenames_to_update.sort()
        for filename in filenames_to_update:
            instructions[f"Update {filename}"] = textwrap.dedent(
                f"""\
                <p>Please search for and replace all <code>TODO:</code> comments in <code>{filename}</code>.</p>
                """,
            )


# ----------------------------------------------------------------------
def _CreateOpenSSFBadgeInstructions(
    instructions: dict[str, str],
) -> None:
    if "{{ python_package_generate_ci_openssf }}".lower() != "true":
        return

    instructions["OpenSSF Best Practices Badge [Basics] (1 of 6)"] = textwrap.dedent(
        """\
        <p>In this step, we will populate the "Basics" section of the OpenSSF Best Practices Badge.</p>
        <ol>
          <li>Visit <a href="https://www.bestpractices.dev/en/projects/{{ python_package_generate_ci_openssf_id }}/edit?criteria_level=0#basics" target="_blank">https://www.bestpractices.dev/en/projects/{{ python_package_generate_ci_openssf_id }}/edit?criteria_level=0#basics</a>.</li>
          <li>
            <p>Search for these options and set them to the following values:</p>
            <p>
              <table>
                <tr>
                  <th>Name</th>
                  <th>Value</th>
                  <th>Additional Info</th>
                </tr>
                <tr>
                  <td>interact</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>contribution</td>
                  <td>Met</td>
                  <td><code>Non-trivial contribution file in repository: &lt;{{github_url }}/blob/main/CONTRIBUTING.md&gt;</code></td>
                </tr>
                <tr>
                  <td>contribution_requirements</td>
                  <td>Met</td>
                  <td><code>{{ github_url }}/blob/main/CONTRIBUTING.md</code></td>
                </tr>
                <tr>
                  <td>What license(s) is the project released under?</td>
                  <td>{{ documentation_license }}</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>floss_license</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>floss_license_osi</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>license_location</td>
                  <td>Met</td>
                  <td><code>Non-trivial license location file in repository: &lt;{{ github_url }}/blob/main/LICENSE.txt&gt;</code></td>
                </tr>
                <tr>
                  <td>discussion</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>english</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
              </table>
            </p>
          </li>
          <li>Click the "Submit (and exit)" button.</li>
        </ol>
        """,
    )

    instructions["OpenSSF Best Practices Badge [Change Control] (2 of 6)"] = textwrap.dedent(
        """\
        <p>In this step, we will populate the "Change Control" section of the OpenSSF Best Practices Badge.</p>
        <ol>
          <li>Visit <a href="https://www.bestpractices.dev/en/projects/{{ python_package_generate_ci_openssf_id }}/edit?criteria_level=0#changecontrol" target="_blank">https://www.bestpractices.dev/en/projects/{{ python_package_generate_ci_openssf_id }}/edit?criteria_level=0#changecontrol</a>.</li>
          <li>
            <p>Search for these options and set them to the following values:</p>
            <p>
              <table>
                <tr>
                  <th>Name</th>
                  <th>Value</th>
                  <th>Additional Info</th>
                </tr>
                <tr>
                  <td>repo_public</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>repo_track</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>repo_interim</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>repo_distributed</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>version_unique</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>version_semver</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>version_tags</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>release_notes</td>
                  <td>Met</td>
                  <td><code>{{ github_url }}/releases/latest</code></td>
                </tr>
              </table>
            </p>
          </li>
          <li>Click the "Submit (and exit)" button.</li>
        </ol>
        """,
    )

    instructions["OpenSSF Best Practices Badge [Reporting] (3 of 6)"] = textwrap.dedent(
        """\
        <p>In this step, we will populate the "Reporting" section of the OpenSSF Best Practices Badge.</p>
        <ol>
          <li>Visit <a href="https://www.bestpractices.dev/en/projects/{{ python_package_generate_ci_openssf_id }}/edit?criteria_level=0#reporting" target="_blank">https://www.bestpractices.dev/en/projects/{{ python_package_generate_ci_openssf_id }}/edit?criteria_level=0#reporting</a>.</li>
          <li>
            <p>Search for these options and set them to the following values:</p>
            <p>
              <table>
                <tr>
                  <th>Name</th>
                  <th>Value</th>
                  <th>Additional Info</th>
                </tr>
                <tr>
                  <td>report_process</td>
                  <td>Met</td>
                  <td><code>{{ github_url }}/blob/main/CONTRIBUTING.md</code></td>
                </tr>
                <tr>
                  <td>report_tracker</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>report_responses</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>report_archive</td>
                  <td>Met</td>
                  <td><code>{{ github_url }}/issues</code></td>
                </tr>
                <tr>
                  <td>vulnerability_report_process</td>
                  <td>Met</td>
                  <td><code>{{ github_url }}/blob/main/SECURITY.md</code></td>
                </tr>
                <tr>
                  <td>vulnerability_report_private</td>
                  <td>Met</td>
                  <td><code>{{ github_url }}/blob/main/SECURITY.md</code></td>
                </tr>
              </table>
            </p>
          </li>
          <li>Click the "Submit (and exit)" button.</li>
        </ol>
        """,
    )

    instructions["OpenSSF Best Practices Badge [Quality] (4 of 6)"] = textwrap.dedent(
        """\
        <p>In this step, we will populate the "Quality" section of the OpenSSF Best Practices Badge.</p>
        <ol>
          <li>Visit <a href="https://www.bestpractices.dev/en/projects/{{ python_package_generate_ci_openssf_id }}/edit?criteria_level=0#quality" target="_blank">https://www.bestpractices.dev/en/projects/{{ python_package_generate_ci_openssf_id }}/edit?criteria_level=0#quality</a>.</li>
          <li>
            <p>Search for these options and set them to the following values:</p>
            <p>
              <table>
                <tr>
                  <th>Name</th>
                  <th>Value</th>
                  <th>Additional Info</th>
                </tr>
                <tr>
                  <td>build</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>build_common_tools</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>build_floss_tools</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>test</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>test_invocation</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>test_most</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>test_continuous_integration</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>test_policy</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>tests_are_added</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>tests_documented_added</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>warnings</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>warnings_fixed</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>warnings_strict</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
              </table>
            </p>
          </li>
          <li>Click the "Submit (and exit)" button.</li>
        </ol>
        """,
    )

    instructions["OpenSSF Best Practices Badge [Analysis] (5 of 6)"] = textwrap.dedent(
        """\
        <p>In this step, we will populate the "Analysis" section of the OpenSSF Best Practices Badge.</p>
        <ol>
          <li>Visit <a href="https://www.bestpractices.dev/en/projects/{{ python_package_generate_ci_openssf_id }}/edit?criteria_level=0#analysis" target="_blank">https://www.bestpractices.dev/en/projects/{{ python_package_generate_ci_openssf_id }}/edit?criteria_level=0#analysis</a>.</li>
          <li>
            <p>Search for these options and set them to the following values:</p>
            <p>
              <table>
                <tr>
                  <th>Name</th>
                  <th>Value</th>
                  <th>Additional Info</th>
                </tr>
                <tr>
                  <td>static_analysis</td>
                  <td>Met</td>
                  <td><code>pylint, CodeQL</code></td>
                </tr>
                <tr>
                  <td>static_analysis_common_vulnerabilities</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>static_analysis_often</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>dynamic_analysis</td>
                  <td>Met</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td>dynamic_analysis_unsafe</td>
                  <td>N/A</td>
                  <td>&nbsp;</td>
                </tr>
              </table>
            </p>
          </li>
          <li>Click the "Submit (and exit)" button.</li>
        </ol>
        """,
    )

    instructions["OpenSSF Best Practices Badge [Manual Changes] (6 of 6)"] = textwrap.dedent(
        """\
        <p>In this step, we will manually populate the remaining questions across all sections of the OpenSSF Best Practices Badge.</p>
        <ol>
          <li>Visit <a href="https://www.bestpractices.dev/en/projects/{{ python_package_generate_ci_openssf_id }}/edit?criteria_level=0" target="_blank">https://www.bestpractices.dev/en/projects/{{ python_package_generate_ci_openssf_id }}/edit?criteria_level=0</a>.</li>
          <li>Update the remaining questions in all sections basic on information specific to your project.</li>
        </ol>
        """,
    )


# ----------------------------------------------------------------------
def _CreatePostFinalInstructions(
    instructions: dict[str, str],
) -> None:
    instructions["Delete this file"] = textwrap.dedent(
        """\
        <p>After you have completed all the steps, you can delete this file.</p>
        <p>Now your project is ready to go!</p>
        """,
    )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    MoveContent()

    UpdatePostGenerationActionsFile()

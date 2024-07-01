import os
import stat
import sys
import textwrap

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
output_dir = Path.cwd()
bootstrapper_script = EnsureFile(output_dir / "Bootstrap.sh")

if os.name == "nt":
{% if repository_tool == 'None' %}
    pass # Nothing to do here
{% elif repository_tool == 'git' %}
    # We have to add an instruction for the user to set the permissions manually, as Windows doesn't
    # have the necessary file permissions. We can't set it programmatically as the file must be
    # added to git before the permissions can be set.
    AugmentFile(
        EnsureFile(output_dir / "__git_precommit_permissions.txt"),
        f"{bootstrapper_script.name}\n",
        None,
    )

{% else %}
    raise Exception("Implement this code for the repository tool being used.")
{% endif %}

else:
    bootstrapper_script.chmod(
        bootstrapper_script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
    )


# ----------------------------------------------------------------------
# Update the repository ignore file
{% if repository_tool == 'None' %}
# Nothing to do here
{% elif repository_tool == 'git' %}
AugmentFile(
    EnsureFile(output_dir / ".gitignore"),
    textwrap.dedent(
        """\
        Activate*.cmd
        Activate*.sh
        Deactivate*.cmd
        Deactivate*.sh

        **/__pycache__/**
        **/Generated/**

        """,
    ),
    None,
)
{% else %}
raise Exception("Implement this code for the repository tool being used.")
{% endif %}


# ----------------------------------------------------------------------
{% if generate_docs %}
development_filename = EnsureFile(output_dir / "DEVELOPMENT.md")

steps: list[str] = []

{% if hosting_platform == 'None' %}
# Nothing to do here
{% elif hosting_platform == 'GitHub' %}
steps.append(
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
{% else %}
raise Exception("Implement this code for the hosting platform being used.")
{% endif %}

step_offset = len(steps)

steps += [
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

AugmentFile(
    development_filename,
    textwrap.dedent(
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
    ).format(''.join(steps).rstrip()),
    "Enlistment",
    AugmentFileStyle.Finalize,
)

{% endif %}

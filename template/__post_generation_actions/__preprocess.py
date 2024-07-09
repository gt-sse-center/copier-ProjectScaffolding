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

    # Commit instructions
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
            if os.name == "nt":
                {% if not _git_suppress_permission_instructions %}
                if shell_scripts:
                    precommit_permissions = "{}<br/>\n".format("<br/>\n".join(f'{commit_step_num + index}. <code>git update-index --chmod=+x "{script.relative_to(Path.cwd())}"</code>' for index, script in enumerate(shell_scripts)))

                    commit_step_num += len(shell_scripts)
                    push_step_num += len(shell_scripts)
                {% else %}
                pass
                {% endif %}
            else:
                for shell_script in shell_scripts:
                    shell_script.chmod(
                        shell_script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
                    )

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

    # Project-specific instructions
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

    # Documentation instructions
    {% if generate_docs %}
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
    {% endif %}

    # Final instructions
    instructions["Delete this file"] = textwrap.dedent(
        """\
        <p>After you have completed all the steps, you can delete this file.</p>
        <p>Now your project is ready to go!</p>
        """,
    )

    # Update the file
    post_generation_actions_filename = EnsureFile(Path.cwd() / "post_generation_actions.html")

    content = post_generation_actions_filename.read_text(encoding="utf-8")

    content = ReplaceContent(
        post_generation_actions_filename.suffix,
        "Instructions",
        content,
        "\n".join(
            textwrap.dedent(
                """\
                <details>
                    <summary>
                        <span role="term"><input type="checkbox" id="{title_id}">{title}</span>
                    </summary>
                </details>
                <div role="definition" class="details-content">
                    {steps_html}
                </div>
                """
            ).format(
                title_id=title.lower().replace(' ', '-'),
                title=title,
                steps_html=instruction,
            )
            for title, instruction in instructions.items()
        ),
    )

    post_generation_actions_filename.write_text(content, encoding="utf-8")


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    MoveContent()

    UpdatePostGenerationActionsFile()

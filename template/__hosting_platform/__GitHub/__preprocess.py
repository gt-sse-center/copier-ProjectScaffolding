import sys
import textwrap

from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "__tools"))
from CopierHelpers import *


# ----------------------------------------------------------------------
if "{{ repository_tool }}" != "git":
    sys.stderr.write("\nERROR: repository_tool should be set to 'git' when hosting_platform is set to '{{ hosting_platform }}' (it is currently set to '{{ repository_tool }}').\n\n")
    sys.exit(-1)


# ----------------------------------------------------------------------
output_dir = Path.cwd()


# ----------------------------------------------------------------------
# |
# |  Documentation
# |
# ----------------------------------------------------------------------
{% if generate_docs %}


# ----------------------------------------------------------------------
contributing_filename = EnsureFile(output_dir / "CONTRIBUTING.md")

AugmentFile(
    contributing_filename,
    "For specific proposals, please provide them as [pull requests](https://github.com/coreinfrastructure/best-practices-badge/pulls) or [issues](https://github.com/coreinfrastructure/best-practices-badge/issues) via our [GitHub site]({{ github_url }}).\n",
    "General Information",
    AugmentFileStyle.Finalize,
)

AugmentFile(
    contributing_filename,
    textwrap.dedent(
        """\
        Pull requests are preferred, since they are specific. For more about how to create a pull request, see https://help.github.com/articles/using-pull-requests/.

        We recommend creating different branches for different (logical) changes, and creating a pull request into the `main` branch when you're done. See the GitHub documentation on [creating branches](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/) and [using pull requests](https://help.github.com/articles/using-pull-requests/).
        """,
    ),
    "Pull Requests and Branches",
    AugmentFileStyle.Finalize,
)

AugmentFile(
    contributing_filename,
    "We use GitHub to track proposed changes via its [issue tracker](https://github.com/coreinfrastructure/best-practices-badge/issues) and [pull requests](https://github.com/coreinfrastructure/best-practices-badge/pulls). Specific changes are proposed using those mechanisms. Issues are assigned to an individual, who works and then marks it complete. If there are questions or objections, the conversation of that issue or pull request is used to resolve it.\n",
    "Proposals",
    AugmentFileStyle.Finalize,
)

# ----------------------------------------------------------------------
security_filename = EnsureFile(output_dir / "SECURITY.md")

AugmentFile(
    security_filename,
    textwrap.dedent(
        '''\
        We prefer that you use the [GitHub mechanism for privately reporting a vulnerability](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability#privately-reporting-a-security-vulnerability). Under the [main repository's security tab]({{ github_url }}/security), in the left sidebar, under "Reporting", click "Advisories", click the "New draft security advisory" button to open the advisory form.
        [issues](https://github.com/coreinfrastructure/best-practices-badge/issues) via our [GitHub site]({{ github_url }}).
        ''',
    ),
    "Submit Vulnerability",
    AugmentFileStyle.Finalize,
)


{% endif %}

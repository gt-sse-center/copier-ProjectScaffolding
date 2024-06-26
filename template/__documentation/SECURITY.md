# Security

If you find a significant vulnerability, or evidence of one, please report it privately.

{% if hosting_platform == 'None' %}
TODO: Include information on how to securely submit a vulnerability.
{%- elif hosting_platform == 'GitHub' -%}
We prefer that you use the [GitHub mechanism for privately reporting a vulnerability](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability#privately-reporting-a-security-vulnerability). Under the [main repository's security tab]({{ github_url }}/security), in the left sidebar, under "Reporting", click "Advisories", click the "New draft security advisory" button to open the advisory form.
[issues](https://github.com/coreinfrastructure/best-practices-badge/issues) via our [GitHub site]({{ github_url }}).
{%- else -%}
{{ "Define this section for your 'hosting_platform'." | raise_exception }}
{%- endif -%}

We will gladly give credit to anyone who reports a vulnerability so that we can fix it. If you want to remain anonymous or pseudonymous instead, please let us know that; we will gladly respect your wishes.

We gladly welcome patches to fix such vulnerabilities! See [CONTRIBUTING.md](CONTRIBUTING.md) for information about contributions.

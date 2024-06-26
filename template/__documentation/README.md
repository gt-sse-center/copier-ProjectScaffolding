# {{ project_name }}

<!-- BEGIN: Exclude Package -->
{% if hosting_platform == 'None' -%}
{% elif hosting_platform == 'GitHub' -%}
[![License](https://img.shields.io/github/license/{{ github_username }}/{{ github_repo_name }}?color=dark-green)]({{ github_url }}/blob/master/LICENSE.txt)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/{{ github_username }}/{{ github_repo_name }}?color=dark-green)]({{ github_url }}/commits/main/)
{% else %}
{{ "Define this section for your 'hosting_platform'." | raise_exception }}
{% endif -%}
<!-- [BEGIN] Badges -->
<!-- [END] Badges -->
<!-- END: Exclude Package -->

{% if project_description -%}
{{ project_description }}
{%- endif %}

<!-- BEGIN: Exclude Package -->
## Contents
- [Overview](#overview)
- [Installation](#installation)
- [Development](#development)
- [Additional Information](#additional-information)
- [License](#license)
<!-- END: Exclude Package -->

## Overview
TODO: Complete this section

### How to use {{ project_name }}
TODO: Complete this section

<!-- BEGIN: Exclude Package -->
## Installation
<!-- [BEGIN] Installation -->
<!-- [END] Installation -->

## Development
{% if hosting_platform == 'None'-%}
Please visit CONTRIBUTING.md and DEVELOPMENT.md for information on contributing to this project.
{% elif hosting_platform == 'GitHub' -%}
Please visit [Contributing]({{ github_url }}/blob/main/CONTRIBUTING.md) and [Development]({{ github_url }}/blob/main/DEVELOPMENT.md) for information on contributing to this project.
{% else %}
{{ "Define this section for your 'hosting_platform'." | raise_exception }}
{% endif -%}

<!-- END: Exclude Package -->

## Additional Information
Additional information can be found at these locations.

| Title | Document | Description |
| --- | --- | --- |
{% if hosting_platform == 'None' -%}
| Code of Conduct | CODE_OF_CONDUCT.md | Information about the the norms, rules, and responsibilities we adhere to when participating in this open source community. |
| Contributing | CONTRIBUTING.md | Information about contributing code changes to this project. |
| Development | DEVELOPMENT.md | Information about development activities involved in making changes to this project. |
| Governance | GOVERNANCE.md | Information about how this project is governed. |
| Maintainers | MAINTAINERS.md | Information about individuals who maintain this project. |
| Security | SECURITY.md | Information about how to privately report security issues associated with this project. |
{% elif hosting_platform == 'GitHub' -%}
| Code of Conduct | [CODE_OF_CONDUCT.md]({{ github_url }}/blob/main/CODE_OF_CONDUCT.md) | Information about the the norms, rules, and responsibilities we adhere to when participating in this open source community. |
| Contributing | [CONTRIBUTING.md]({{ github_url }}/blob/main/CONTRIBUTING.md) | Information about contributing code changes to this project. |
| Development | [DEVELOPMENT.md]({{ github_url }}/blob/main/DEVELOPMENT.md) | Information about development activities involved in making changes to this project. |
| Governance | [GOVERNANCE.md]({{ github_url }}/blob/main/GOVERNANCE.md) | Information about how this project is governed. |
| Maintainers | [MAINTAINERS.md]({{ github_url }}/blob/main/MAINTAINERS.md) | Information about individuals who maintain this project. |
| Security | [SECURITY.md]({{ github_url }}/blob/main/SECURITY.md) | Information about how to privately report security issues associated with this project. |
{% else %}
{{ "Define this section for your 'hosting_platform'." | raise_exception }}
{% endif -%}

## License

{{ project_name }} is licensed under the <a href="
{%- if documentation_license == "MIT" -%}
    https://choosealicense.com/licenses/mit/
{%- elif documentation_license == "Apache-2.0" -%}
    https://choosealicense.com/licenses/apache-2.0/
{%- elif documentation_license == "BSD-3-Clause-Clear" -%}
    https://choosealicense.com/licenses/bsd-3-clause-clear/
{%- elif documentation_license == "GPL-3.0-or-later" -%}
    https://choosealicense.com/licenses/gpl-3.0/
{%- elif documentation_license == "BSL-1.0" -%}
    https://choosealicense.com/licenses/bsl-1.0/
{%- endif -%}
" target="_blank">{{ documentation_license }}</a> license.

# {{ project_name }}

<!-- BEGIN: Exclude Package -->
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
<!-- [BEGIN] Development -->
<!-- [END] Development -->

<!-- END: Exclude Package -->

## Additional Information
Additional information can be found at these locations.

| Title | Document | Description |
| --- | --- | --- |
<!-- [BEGIN] Additional Information -->
<!-- [END] Additional Information -->

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

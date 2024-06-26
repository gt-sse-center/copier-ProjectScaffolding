# Local Development

## Enlistment
{% if hosting_platform == 'None' -%}
TODO: Populate the enlistment section
{%- elif hosting_platform == 'GitHub' -%}
<!-- [BEGIN] Populate Enlistment -->
<!-- [END] Populate Enlistment -->
{%- else -%}
{{ "Define this section for your 'hosting_platform'." | raise_exception }}
{%- endif %}

## Development Activities
{% if hosting_platform == 'None' -%}
TODO: Populate the development activities section
{%- elif hosting_platform == 'GitHub' -%}
<!-- [BEGIN] Populate Development Activities -->
<!-- [END] Populate Development Activities -->
{%- else -%}
{{ "Define this section for your 'hosting_platform'." | raise_exception }}
{%- endif %}

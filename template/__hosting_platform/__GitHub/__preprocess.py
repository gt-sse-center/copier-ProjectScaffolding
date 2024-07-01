import sys


# ----------------------------------------------------------------------
if "{{ repository_tool }}" != "git":
    sys.stderr.write("\nERROR: repository_tool should be set to 'git' when hosting_platform is set to '{{ hosting_platform }}' (it is currently set to '{{ repository_tool }}').\n\n")
    sys.exit(-1)

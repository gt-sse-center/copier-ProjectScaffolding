import re
import unicodedata

from typing import Protocol

from jinja2.ext import Extension


class IfyFuncType(Protocol):
    def __call__(self, value: str, allow_unicode: bool = False) -> str: ...


# taken from Django
# https://github.com/django/django/blob/main/django/utils/text.py
def create_ify_func(
    separator: str,
) -> IfyFuncType:
    # ----------------------------------------------------------------------
    def ify(value: str, allow_unicode: bool = False) -> str:
        """
        Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
        dashes to single dashes. Remove characters that aren't alphanumerics,
        underscores, or hyphens. Convert to lowercase. Also strip leading and
        trailing whitespace, dashes, and underscores.
        """
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize("NFKC", value)
        else:
            value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
        value = re.sub(r"[^\w\s-]", "", value)
        return re.sub(r"[-\s]+", separator, value).strip("-_")

    # ----------------------------------------------------------------------

    return ify


class SlugifyExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["slugify"] = create_ify_func("-")


class PythonifyExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["pythonify"] = create_ify_func("_")

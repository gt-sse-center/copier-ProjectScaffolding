from jinja2.ext import Extension


# ----------------------------------------------------------------------
class QuoteEscaper(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["escape_quotes"] = lambda value, allow_unicode=False: value.replace(
            '"', '\\"'
        )


# ----------------------------------------------------------------------
class TickEscaper(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["escape_ticks"] = lambda value, allow_unicode=False: value.replace(
            "'", "\\'"
        )

from jinja2.ext import Extension


def raise_exception(value):
    raise Exception(value)


class ExceptionExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["raise_exception"] = raise_exception

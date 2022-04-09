import functools

from click import ClickException


def exceptions(func):
    """Handle application exceptions and raises them as ClickExceptions."""

    @functools.wraps(func)
    def wrapper_exceptions(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            raise ClickException(e)

    return wrapper_exceptions

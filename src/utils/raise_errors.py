"""Errors"""

# utilities
from src.utils.application_error import ApplicationError


def raises(message, status_code):
    """A helper method for raising exceptions.
    Args:
        message (str): Message
        status_code (int): Status code
    Raises:
        ValidationError
    """
    raise ApplicationError(message, status_code)

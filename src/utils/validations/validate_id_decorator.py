"""validate params ID module"""

from functools import wraps
import re

from src.utils.constants import ERROR_MESSAGES
from src.utils.raise_errors import raises


def is_valid_id(id_):
    """Check if id is valid"""
    return re.match(r'^[\-a-zA-Z0-9_]{20}', id_)


def check_id_valid(**kwargs):
    """Check if id is valid"""
    for key in kwargs:
        if key.endswith('_id') and not is_valid_id(kwargs.get(key, None)):
            raises(ERROR_MESSAGES['INVALID_ID'], 400)


def validate_id(func):
    """Decorator function for views to validate id"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """Function with decorated function mutations."""
        check_id_valid(**kwargs)
        return func(*args, **kwargs)

    return decorated_function

"""No space validator module"""
import re

# third party imports
from marshmallow import ValidationError

from src.utils.constants import ERROR_MESSAGES

REG = re.compile(r'[\s]')


def no_space_validation(data):
    """Validates the email"""
    if REG.search(data):
        raise ValidationError(ERROR_MESSAGES['NO_SPACE'])

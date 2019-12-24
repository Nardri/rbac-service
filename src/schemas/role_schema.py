"""Module for role schema"""

# third party imports
from marshmallow import fields, validate

from src.schemas import BaseSchema
from src.utils.validations import no_space_validation


class RoleSchema(BaseSchema):
    """Role schema"""
    name = fields.String(
        required=True,
        validate=[validate.Length(min=3, max=100), no_space_validation])
    is_default = fields.Boolean(required=False, data_key='isDefault')

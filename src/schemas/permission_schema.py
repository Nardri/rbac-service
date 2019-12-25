"""Module for role schema"""

# third party imports
from marshmallow import fields, validates, ValidationError
from marshmallow_enum import EnumField

from src.models.permission import PermissionType
from src.schemas import BaseSchema
from src.utils.constants import ERROR_MESSAGES
from src.utils.validations.validate_id_decorator import is_valid_id


class PermissionSchema(BaseSchema):
    """Role schema"""

    type = EnumField(PermissionType,
                     required=True,
                     error='"{input}" must be one of: [{names}]')

    service_id = fields.String(load_only=True,
                               required=True,
                               data_key='serviceId')

    service = fields.Nested('ServiceSchema', dump_only=True)

    @validates('service_id')
    def validate_service_id(self, value):
        """validate id"""

        if not is_valid_id(value):
            raise ValidationError(ERROR_MESSAGES['INVALID_ID'])

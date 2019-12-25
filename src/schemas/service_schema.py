"""Service schema module"""

from marshmallow import fields, validate, post_load
from src.schemas import BaseSchema


class ServiceSchema(BaseSchema):
    """Schema class"""

    name = fields.String(required=True,
                         validate=[validate.Length(min=3, max=100)])

    @post_load
    def append_service_to_name(self, data, **kwargs):
        """Append service to the service name"""

        data['name'] = f'{data.get("name").upper()}_SERVICE'
        return data

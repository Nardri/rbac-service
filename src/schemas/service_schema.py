"""Service schema module"""

from marshmallow import fields, validate
from src.schemas import BaseSchema


class ServiceSchema(BaseSchema):
    """Schema class"""

    name = fields.String(required=True,
                         validate=[validate.Length(min=3, max=100)])

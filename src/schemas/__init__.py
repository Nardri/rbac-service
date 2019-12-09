"""Module for all base schemas"""
import typing

from marshmallow import fields, Schema, ValidationError

from src.utils.raise_errors import raises


class BaseSchema(Schema):
    """Base schema for all schemas."""

    id = fields.String(dump_only=True)

    created_at = fields.DateTime(dump_only=True, data_key='createdAt')
    updated_at = fields.DateTime(dump_only=True, data_key='updatedAt')

    def handle_error(self, error: ValidationError, data: typing.Any, *,
                     many: bool, **kwargs):
        """Error handler."""

        raise raises(error.messages, status_code=400)

    class Meta:
        """Meta Class"""

        ordered = True

"""Data transfer object"""

from flask_restplus import fields, Namespace


class RoleDto:
    """Role data transfer object."""

    role_ns = Namespace('role', description='Role related operations')
    role_dto = role_ns.model(
        'Role', {
            'name': fields.String(required=True, min=3, max=100),
            'isDefault': fields.Boolean(required=False)
        })

    role_model = role_ns.model(
        'RoleModel', {
            "id": fields.String,
            "name": fields.String,
            "isDefault": fields.Boolean,
            "createdAt": fields.DateTime,
            "updatedAt": fields.DateTime,
        })

    role_response = role_ns.model(
        'RoleResponse', {
            "status": fields.String,
            "message": fields.String,
            "data": fields.Nested(role_model)
        })

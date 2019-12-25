"""Data transfer object"""

from flask_restplus import fields, Namespace

from src.models.permission import PermissionType


class RoleDto:
    """Role data transfer object."""

    role_ns = Namespace('role', description='Role related operations')
    role_dto = role_ns.model(
        'Role', {
            'name': fields.String(required=True, min=3, max=100),
            'isDefault': fields.Boolean(required=False)
        })

    permission_dto = role_ns.model(
        'Permission', {
            'type':
            fields.String(description='The permission type',
                          enum=PermissionType.get_enum_member_names()),
            'serviceId':
            fields.String(required=True)
        })

    role_model = role_ns.model(
        'RoleModel', {
            "id": fields.String,
            "name": fields.String,
            "isDefault": fields.Boolean,
            "createdAt": fields.DateTime,
            "updatedAt": fields.DateTime,
        })

    service = role_ns.model('ServiceModel', {
        'id': fields.String,
        "name": fields.String,
    })

    permission = role_ns.model(
        'PermissionModel', {
            'id': fields.String,
            "type": fields.String,
            "service": fields.Nested(service)
        })

    role_model_with_perm = role_ns.model(
        'RoleModelI', {
            "id": fields.String,
            "name": fields.String,
            "createdAt": fields.DateTime,
            "updatedAt": fields.DateTime,
            "permissions": fields.Nested(permission)
        })

    role_response = role_ns.model(
        'RoleResponse', {
            "status": fields.String,
            "message": fields.String,
            "data": fields.Nested(role_model)
        })
    role_response_I = role_ns.model(
        'RoleResponse', {
            "status": fields.String,
            "message": fields.String,
            "data": fields.Nested(role_model_with_perm)
        })

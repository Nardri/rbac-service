"""Roles Resource Module"""

# third party library
from flask import request

# Local imports
from src.models import Role, Permission, Service
from src.models.permission import PermissionType
from src.schemas import RoleSchema, PermissionSchema, RoleWithPermissionSchema
from src.utils.api_response import response
from src.utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES
from src.utils.validations import validate_id
from src.utils.misc import get_service_name
from src.utils.raise_errors import raises
from src.dto import RoleDto
from src.views.base.base_resource import BaseResource

ROLE_NS = RoleDto.role_ns
ROLE_DTO = RoleDto.role_dto
PERMISSION_DTO = RoleDto.permission_dto
ROLE_RESPONSE = RoleDto.role_response
ROLE_RESPONSE_I = RoleDto.role_response_I


@ROLE_NS.route('/')
class RoleListResource(BaseResource):
    """Roles Resource"""

    # instantiate the role schema
    schema = RoleSchema()
    model = Role

    @ROLE_NS.doc('list_roles')
    @ROLE_NS.marshal_list_with(ROLE_RESPONSE)
    def get(self):
        """Get roles"""

        roles = self.get_queryset().all()
        serialized_roles = self.schema.dump(roles, many=True)
        return response(serialized_roles,
                        SUCCESS_MESSAGES['FETCHED'].format('roles'))

    @ROLE_NS.doc('Create Role')
    @ROLE_NS.expect(ROLE_DTO, validate=True)
    @ROLE_NS.marshal_with(ROLE_RESPONSE, code=201)
    def post(self):
        """Create a new role"""

        # get the request data in json format
        request_json = request.get_json()

        # serialize and validate the request
        role_details = self.schema.load(request_json)
        role_details['name'] = role_details['name'].strip().lower()

        role = self.model.query_(name=role_details['name']).first()
        if role:
            raises(ERROR_MESSAGES['DUPLICATES'].format('role'), 409)

        saved_role = self.model(**role_details).save()
        new_role = self.schema.dump(saved_role)

        if saved_role:
            return response(new_role, status_code=201, object_name='role')


parser = ROLE_NS.parser()
parser.add_argument('include',
                    type=str,
                    choices=['permissions'],
                    help='Include permissions in the response',
                    location='args')


@ROLE_NS.route('/<string:role_id>')
@ROLE_NS.response(404, 'Role not found.')
@ROLE_NS.param('role_id', 'The role identifier')
class RoleResource(BaseResource):
    """Roles Resource"""

    schema = RoleSchema()
    model = Role

    @ROLE_NS.doc(
        'Get a role',
        responses={
            201: 'Success',
            400: 'Missing parameter',
            403: 'Insufficient permissions',
            500: 'Internal failure',
        },
    )
    @ROLE_NS.expect(parser)
    @ROLE_NS.response(code=200, model=ROLE_RESPONSE_I, description='success I')
    @validate_id
    def get(self, role_id):
        """Get a role"""

        args = parser.parse_args(request)
        role = self.get_object(role_id)

        if 'include' in args and args.get('include') == 'permissions':
            schema = RoleWithPermissionSchema()
            serialized_roles = schema.dump(role)
        else:
            serialized_roles = self.schema.dump(role)
        return response(serialized_roles,
                        SUCCESS_MESSAGES['FETCHED'].format('role'))

    @ROLE_NS.doc('Update Role')
    @ROLE_NS.expect(ROLE_DTO, validate=True)
    @ROLE_NS.response(200, 'Successfully updated role')
    @validate_id
    def patch(self, role_id):
        """Update a role"""

        # get the request data in json format
        request_json = request.get_json()

        # serialize and validate the request
        role_details = self.schema.load(request_json)
        role_details['name'] = role_details['name'].strip().lower()

        found_role = self.model.query_(name=role_details['name']).first()

        if found_role:
            raises(ERROR_MESSAGES['DUPLICATES'].format('role'), 409)

        role = self.get_object(role_id)
        role.update_(**role_details)
        return response(message=SUCCESS_MESSAGES['UPDATE'].format('role'))

    @ROLE_NS.doc('Delete Role')
    @ROLE_NS.response(204, 'Role Deleted.')
    @validate_id
    def delete(self, role_id):
        """Delete a role"""

        role = self.get_object(role_id)
        deleted_role = self.model.delete(role)
        return response(
            message=SUCCESS_MESSAGES['DELETE'].format(deleted_role.name))


@ROLE_NS.route('/<string:role_id>/permission')
@ROLE_NS.response(404, 'Role not found.')
@ROLE_NS.param('role_id', 'The role identifier')
class RolePermissionResource(BaseResource):
    """Resource for assigning permissions to role."""

    model = Permission
    schema = PermissionSchema()

    @ROLE_NS.doc('Create permission for role')
    @ROLE_NS.expect(PERMISSION_DTO, validate=False)
    @ROLE_NS.response(201, 'Successfully created permission')
    @validate_id
    def post(self, role_id):
        """Create permission for a role"""

        # get the request data in json format
        request_json = request.get_json()

        # serialize and validate the request
        request_dict = self.schema.load(request_json)

        role_object = Role.query_().get(role_id)

        if not role_object:
            raises(ERROR_MESSAGES['DOES_EXIST'].format('role'), 404)

        service_object = Service.query_().get(request_dict.get('service_id'))
        if not service_object:
            raises(ERROR_MESSAGES['DOES_EXIST'].format('service'), 404)

        permission_type = request_dict.get('type')
        if permission_type is PermissionType.FULL_ACCESS:
            permission = Permission.query.with_parent(
                service_object).filter_by(
                    type=PermissionType.FULL_ACCESS).first()

            if permission:
                raises(
                    ERROR_MESSAGES['ALREADY_HAS_FULL_ACCESS'].format(
                        role_object.name.title(),
                        service_object.name.split('_')[0].title()), 422)

            other_permissions = Permission.query.with_parent(
                service_object).filter(
                    Permission.type != PermissionType.FULL_ACCESS).all()

            if other_permissions:
                for permission in other_permissions:
                    permission.delete()

        else:
            permission_found = Permission.query.with_parent(
                service_object).filter_by(type=permission_type).first()

            if permission_found:
                raises(
                    ERROR_MESSAGES['DUPLICATE_PERMISSION'].format(
                        role_object.name.title(),
                        service_object.name.split('_')[0].title()), 409)

            found_full_access_perm = Permission.query.with_parent(
                service_object).filter_by(
                    type=PermissionType.FULL_ACCESS).first()

            if found_full_access_perm:
                found_full_access_perm.delete()

        request_dict['role'] = role_object
        request_dict['service'] = service_object
        self.model(**request_dict).save()
        return response(status_code=201,
                        message=SUCCESS_MESSAGES['ADDED'].format(
                            permission_type.name, role_object.name.title(),
                            get_service_name(service_object)))

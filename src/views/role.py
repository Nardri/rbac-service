"""Roles Resource Module"""

# third party library
from flask import request

# Local imports
from src.models import Role
from src.schemas import RoleSchema
from src.utils.api_response import response
from src.utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES
from src.utils.validations import validate_id
from src.utils.raise_errors import raises
from src.dto import RoleDto
from src.views.base.base_resource import BaseResource

ROLE_NS = RoleDto.role_ns
ROLE_DTO = RoleDto.role_dto
ROLE_RESPONSE = RoleDto.role_response


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


@ROLE_NS.route('/<string:role_id>')
@ROLE_NS.response(404, 'Role not found.')
@ROLE_NS.param('role_id', 'The role identifier')
class RoleResource(BaseResource):
    """Roles Resource"""

    schema = RoleSchema()
    model = Role

    @ROLE_NS.doc('Get a role')
    @ROLE_NS.marshal_with(ROLE_RESPONSE)
    @validate_id
    def get(self, role_id):
        """Get a role"""

        role = self.get_object(role_id)
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

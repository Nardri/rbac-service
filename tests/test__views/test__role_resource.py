"""Test module for the role endpoints"""

from flask import json
from app import api
from src.factories import ServiceFactory, PermissionFactory

from src.models import Role, Service
from src.models.permission import PermissionType
from src.utils.misc import get_service_name
from src.views.role import (RoleResource, RoleListResource,
                            RolePermissionResource)
from src.factories.role_factory import RoleFactory, RoleWithPermissionFactory
from src.utils.constants import CHARSETS, SUCCESS_MESSAGES, ERROR_MESSAGES

from tests import DisableUniqueIdListener


class TestRoleEndpoints:
    """Test class for the role endpoints."""
    def test__get_roles_succeeds(self, init_db, client):
        """Test for the get all role endpoint."""

        new_roles = RoleFactory.create_batch(size=5)

        url = api.url_for(RoleListResource)
        response_object = client.get(url)
        response = json.loads(response_object.data.decode(CHARSETS[0]))
        data = response.get('data')

        assert response_object.status_code == 200
        assert len(data) == 5
        assert response.get('status') == 'success'
        assert response.get('message') == SUCCESS_MESSAGES['FETCHED'].format(
            'roles')
        assert new_roles[0].name == data[0]['name']

    def test__get_a_role_succeeds(self, init_db, client):
        """Test get a single role"""

        with DisableUniqueIdListener(Role, 'before_insert'):
            new_roles = RoleFactory.create_batch(size=3)
            role_id = new_roles[0].id

            url = api.url_for(RoleResource, role_id=role_id)
            response_object = client.get(url)
            response = json.loads(response_object.data.decode(CHARSETS[0]))
            data = response.get('data')

            assert response_object.status_code == 200
            assert response.get('status') == 'success'
            assert response.get('message') == SUCCESS_MESSAGES['FETCHED'] \
                .format('role')
            assert new_roles[0].name == data['name']

    def test__get_a_role_with_permissions_succeeds(self, init_db, client):
        """Test get a single role"""

        with DisableUniqueIdListener(Role, 'before_insert'):
            new_roles = RoleWithPermissionFactory.create_batch(size=3)
            role_id = new_roles[0].id

            url = api.url_for(RoleResource, role_id=role_id)
            response_object = client.get(url + '?include=permissions')
            response = json.loads(response_object.data.decode(CHARSETS[0]))
            data = response.get('data')

            assert response_object.status_code == 200
            assert response.get('status') == 'success'
            assert response.get('message') == SUCCESS_MESSAGES['FETCHED'] \
                .format('role')
            assert new_roles[0].name == data['name']
            assert len(new_roles[0].permissions) >= 1

    def test__delete_a_role_succeeds(self, init_db, client):
        """Test delete a single role"""

        with DisableUniqueIdListener(Role, 'before_insert'):
            new_roles = RoleFactory.create_batch(size=3)
            role_id = new_roles[0].id

            url = api.url_for(RoleResource, role_id=role_id)
            response_object = client.delete(url)
            response = json.loads(response_object.data.decode(CHARSETS[0]))

            assert response_object.status_code == 200
            assert response.get('status') == 'success'
            assert response.get('message') == SUCCESS_MESSAGES['DELETE'] \
                .format(new_roles[0].name)

    def test__get_a_role_with_invalid_id_fails(self, init_db, client):
        """Test delete a single role with invalid id"""

        url = api.url_for(RoleResource, role_id='invalid-id')
        response_object = client.get(url)
        response = json.loads(response_object.data.decode(CHARSETS[0]))
        assert response_object.status_code == 400
        assert response.get('status') == 'error'
        assert response.get('error') == ERROR_MESSAGES['INVALID_ID']

    def test__delete_a_role_with_invalid_id_fails(self, init_db, client):
        """Test delete a single role with invalid id"""

        url = api.url_for(RoleResource, role_id='invalid-id')
        response_object = client.delete(url)
        response = json.loads(response_object.data.decode(CHARSETS[0]))
        assert response_object.status_code == 400
        assert response.get('status') == 'error'
        assert response.get('error') == ERROR_MESSAGES['INVALID_ID']

    def test__get_a_role_with_unknown_id_fails(self, init_db, client):
        """Test delete a single role with unknown id"""

        url = api.url_for(RoleResource, role_id='-KWhBpDWhYHZP-Pxe1Kl')
        response_object = client.get(url)
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 404
        assert response.get('status') == 'error'
        assert response.get('error') == ERROR_MESSAGES['NOT_FOUND']

    def test__delete_a_role_with_unknown_id_fails(self, init_db, client):
        """Test delete a single role with unknown id"""

        url = api.url_for(RoleResource, role_id='-KWhBpDWhYHZP-Pxe1Kl')
        response_object = client.delete(url)
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 404
        assert response.get('status') == 'error'
        assert response.get('error') == ERROR_MESSAGES['NOT_FOUND']

    def test__post_a_role_succeeds(self, init_db, client, headers):
        """Test creating a new role"""

        data = {"name": "test-admin"}
        url = api.url_for(RoleListResource)
        response_object = client.post(url,
                                      headers=headers,
                                      data=json.dumps(data))
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 201
        assert response.get('status') == 'success'
        assert response.get('message') == SUCCESS_MESSAGES['CREATED'] \
            .format('role')

    def test__post_a_role_with_invalid_data_fails(self, init_db, client,
                                                  headers):
        """Test creating a new role"""

        data = {"name": " "}
        url = api.url_for(RoleListResource)
        response_object = client.post(url,
                                      headers=headers,
                                      data=json.dumps(data))
        response = json.loads(response_object.data.decode(CHARSETS[0]))
        error = response.get('error').get('name')

        assert response_object.status_code == 400
        assert response.get('status') == 'error'
        assert error[0] == ERROR_MESSAGES['INVALID_INPUT_NAME']
        assert error[1] == ERROR_MESSAGES['NO_SPACE']

    def test__post_a_role_with_duplicate_data_fails(self, init_db, client,
                                                    headers):
        """Test creating a new role"""
        new_role = RoleFactory()

        data = {"name": new_role.name}
        url = api.url_for(RoleListResource)
        response_object = client.post(url,
                                      headers=headers,
                                      data=json.dumps(data))
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        error = response.get('error')

        assert response_object.status_code == 409
        assert response.get('status') == 'error'
        assert error == ERROR_MESSAGES['DUPLICATES'].format('role')

    def test__update_a_role_succeeds(self, init_db, client, headers):
        """Test creating a new role"""

        with DisableUniqueIdListener(Role, 'before_insert'):
            new_role = RoleFactory()
            role_id = new_role.id
            data = {"name": "updated-admin"}
            url = api.url_for(RoleResource, role_id=role_id)
            response_object = client.patch(url,
                                           headers=headers,
                                           data=json.dumps(data))
            response = json.loads(response_object.data.decode(CHARSETS[0]))

            assert response_object.status_code == 200
            assert response.get('status') == 'success'
            assert response.get('message') == SUCCESS_MESSAGES['UPDATE'] \
                .format('role')

    def test__patch_a_role_with_invalid_data_fails(self, init_db, client,
                                                   headers):
        """Test creating a new role"""
        with DisableUniqueIdListener(Role, 'before_insert'):
            new_role = RoleFactory()
            role_id = new_role.id

            data = {"name": " "}
            url = api.url_for(RoleResource, role_id=role_id)
            response_object = client.patch(url,
                                           headers=headers,
                                           data=json.dumps(data))
            response = json.loads(response_object.data.decode(CHARSETS[0]))
            error = response.get('error').get('name')

            assert response_object.status_code == 400
            assert response.get('status') == 'error'
            assert error[0] == ERROR_MESSAGES['INVALID_INPUT_NAME']
            assert error[1] == ERROR_MESSAGES['NO_SPACE']

    def test__patch_a_role_with_duplicate_data_fails(self, init_db, client,
                                                     headers):
        """Test creating a new role"""
        with DisableUniqueIdListener(Role, 'before_insert'):
            new_role = RoleFactory()
            role_id = new_role.id

            data = {"name": new_role.name}
            url = api.url_for(RoleResource, role_id=role_id)
            response_object = client.patch(url,
                                           headers=headers,
                                           data=json.dumps(data))
            response = json.loads(response_object.data.decode(CHARSETS[0]))

            error = response.get('error')

            assert response_object.status_code == 409
            assert response.get('status') == 'error'
            assert error == ERROR_MESSAGES['DUPLICATES'].format('role')

    def test__grant_permissions_to_a_role_succeeds(self, init_db, client,
                                                   headers):
        """Test that permissions are granted to roles"""

        with DisableUniqueIdListener([Role, Service], 'before_insert'):
            new_role = RoleFactory()
            new_service = ServiceFactory()
            role_id = new_role.id
            service_id = new_service.id

            data = {
                "type": PermissionType.FULL_ACCESS.name,
                "serviceId": service_id
            }
            url = api.url_for(RolePermissionResource, role_id=role_id)
            response_object = client.post(url,
                                          headers=headers,
                                          data=json.dumps(data))
            response = json.loads(response_object.data.decode(CHARSETS[0]))

            assert response_object.status_code == 201
            assert response.get('status') == 'success'
            assert response.get('message') == SUCCESS_MESSAGES['ADDED'] \
                .format(data.get('type'), new_role.name.title(),
                        get_service_name(new_service))

    def test__granting_duplicate_permission_to_role_fails(
        self, init_db, client, headers):
        """Test that duplicate permissions are not added to roles"""

        with DisableUniqueIdListener([Role, Service], 'before_insert'):
            new_role = RoleWithPermissionFactory(
                permissions=PermissionType.WRITE)
            role_id = new_role.id

            data = {
                "type": new_role.permissions[0].type.name,
                "serviceId": new_role.permissions[0].service.id
            }
            url = api.url_for(RolePermissionResource, role_id=role_id)
            response_object = client.post(url,
                                          headers=headers,
                                          data=json.dumps(data))
            response = json.loads(response_object.data.decode(CHARSETS[0]))

            assert response_object.status_code == 409
            assert response.get('status') == 'error'
            assert response.get(
                'error') == ERROR_MESSAGES['DUPLICATE_PERMISSION'].format(
                    new_role.name.title(),
                    get_service_name(new_role.permissions[0].service))

    def test__granting_full_access_permission_to_role_fails(
        self, init_db, client, headers):
        """Test that duplicate permissions are not added to roles"""

        with DisableUniqueIdListener([Role, Service], 'before_insert'):
            new_role = RoleWithPermissionFactory(
                permissions=PermissionType.FULL_ACCESS)
            role_id = new_role.id

            data = {
                "type": new_role.permissions[0].type.name,
                "serviceId": new_role.permissions[0].service.id
            }
            url = api.url_for(RolePermissionResource, role_id=role_id)
            response_object = client.post(url,
                                          headers=headers,
                                          data=json.dumps(data))
            response = json.loads(response_object.data.decode(CHARSETS[0]))

            assert response_object.status_code == 422
            assert response.get('status') == 'error'
            assert response.get(
                'error') == ERROR_MESSAGES['ALREADY_HAS_FULL_ACCESS'].format(
                    new_role.name.title(),
                    get_service_name(new_role.permissions[0].service))

    def test__granting_permission_to_role_with_invalid_service_id_fails(
        self, init_db, client, headers):
        """Test that permissions are not added to role with invalid service id
        """

        with DisableUniqueIdListener([Role, Service], 'before_insert'):
            new_role = RoleWithPermissionFactory(
                permissions=PermissionType.FULL_ACCESS)
            role_id = new_role.id

            data = {
                "type": new_role.permissions[0].type.name,
                "serviceId": 'role_id'
            }
            url = api.url_for(RolePermissionResource, role_id=role_id)
            response_object = client.post(url,
                                          headers=headers,
                                          data=json.dumps(data))
            response = json.loads(response_object.data.decode(CHARSETS[0]))
            error = response.get('error')
            assert response_object.status_code == 400
            assert response.get('status') == 'error'
            assert error.get('serviceId')[0] == ERROR_MESSAGES['INVALID_ID']

    def test__granting_permission_to_role_with_unknown_service_id_fails(
        self, init_db, client, headers):
        """Test that permissions are not added to role with invalid service id
        """

        with DisableUniqueIdListener([Role, Service], 'before_insert'):
            new_role = RoleWithPermissionFactory(
                permissions=PermissionType.FULL_ACCESS)
            role_id = new_role.id

            data = {
                "type": new_role.permissions[0].type.name,
                "serviceId": role_id
            }
            url = api.url_for(RolePermissionResource, role_id=role_id)
            response_object = client.post(url,
                                          headers=headers,
                                          data=json.dumps(data))
            response = json.loads(response_object.data.decode(CHARSETS[0]))

            assert response_object.status_code == 404
            assert response.get('status') == 'error'
            assert response.get(
                'error') == ERROR_MESSAGES['DOES_EXIST'].format('service')

    def test__granting_permission_to_role_with_invalid_role_id_fails(
        self, init_db, client, headers):
        """Test that permissions are not added to roles with invalid role id"""

        with DisableUniqueIdListener([Role, Service], 'before_insert'):
            new_role = RoleWithPermissionFactory(
                permissions=PermissionType.FULL_ACCESS)
            role_id = new_role.permissions[0].service.id

            data = {
                "type": new_role.permissions[0].type.name,
                "serviceId": new_role.permissions[0].service.id
            }
            url = api.url_for(RolePermissionResource, role_id=role_id)
            response_object = client.post(url,
                                          headers=headers,
                                          data=json.dumps(data))
            response = json.loads(response_object.data.decode(CHARSETS[0]))

            assert response_object.status_code == 404
            assert response.get('status') == 'error'
            assert response.get(
                'error') == ERROR_MESSAGES['DOES_EXIST'].format('role')

    def test__grant_full_access_perm_to_role_removes_other_perms_succeeds(
        self, init_db, client, headers):
        """Test that other permissions are delete when a
        full_access perm is assigned"""

        with DisableUniqueIdListener([Role, Service], 'before_insert'):
            new_service = ServiceFactory()
            new_permissions = [
                PermissionFactory(type=PermissionType.WRITE,
                                  service=new_service),
                PermissionFactory(type=PermissionType.READ,
                                  service=new_service)
            ]
            new_role = RoleFactory(permissions=new_permissions)
            role_id = new_role.id
            service_id = new_role.permissions[0].service.id

            data = {
                "type": PermissionType.FULL_ACCESS.name,
                "serviceId": service_id
            }

            url = api.url_for(RolePermissionResource, role_id=role_id)
            response_object = client.post(url,
                                          headers=headers,
                                          data=json.dumps(data))
            response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 201
        assert response.get('status') == 'success'
        assert new_role.permissions[0].type == PermissionType.FULL_ACCESS
        assert len(new_role.permissions) == 1
        assert response.get('message') == SUCCESS_MESSAGES['ADDED'].format(
            new_role.permissions[0].type.name, new_role.name.title(),
            get_service_name(new_service))

    def test__grant_other_perm_to_role_removes_full_access_perms_succeeds(
        self, init_db, client, headers):
        """Test that other permissions are delete when a
        full_access perm is assigned"""

        with DisableUniqueIdListener([Role, Service], 'before_insert'):
            new_service = ServiceFactory()
            new_permission = [
                PermissionFactory(type=PermissionType.FULL_ACCESS,
                                  service=new_service)
            ]
            new_role = RoleFactory(permissions=new_permission)
            role_id = new_role.id
            service_id = new_role.permissions[0].service.id

            data = {"type": PermissionType.EDIT.name, "serviceId": service_id}

            url = api.url_for(RolePermissionResource, role_id=role_id)
            response_object = client.post(url,
                                          headers=headers,
                                          data=json.dumps(data))
            response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 201
        assert response.get('status') == 'success'
        assert new_role.permissions[0].type == PermissionType.EDIT
        assert len(new_role.permissions) == 1
        assert response.get('message') == SUCCESS_MESSAGES['ADDED'].format(
            new_role.permissions[0].type.name, new_role.name.title(),
            get_service_name(new_service))

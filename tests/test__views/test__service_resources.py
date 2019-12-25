"""Test module for the service endpoints"""

from flask import json
from app import api

from src.models import Service
from src.views import ServiceResource, ServiceListResource
from src.factories import ServiceFactory
from src.utils.constants import CHARSETS, SUCCESS_MESSAGES, ERROR_MESSAGES

from tests import DisableUniqueIdListener


# yapf: disable=W0613
class TestServiceEndpoints:
    """Test class for the service endpoints."""

    def test__get_services_succeeds(self, init_db, client):
        """Test for the get all service endpoint."""

        new_services = ServiceFactory.create_batch(size=5)

        url = api.url_for(ServiceListResource)
        response_object = client.get(url)
        response = json.loads(response_object.data.decode(CHARSETS[0]))
        data = response.get('data')

        assert response_object.status_code == 200
        assert len(data) == 5
        assert response.get('status') == 'success'
        assert response.get('message') == SUCCESS_MESSAGES['FETCHED'].format(
            'services')
        assert new_services[0].name == data[0]['name']

    def test__get_a_service_succeeds(self, init_db, client):
        """Test get a single service"""

        with DisableUniqueIdListener(Service, 'before_insert'):
            new_services = ServiceFactory.create_batch(size=3)
            service_id = new_services[0].id

            url = api.url_for(ServiceResource, service_id=service_id)
            response_object = client.get(url)
            response = json.loads(response_object.data.decode(CHARSETS[0]))
            data = response.get('data')

            assert response_object.status_code == 200
            assert response.get('status') == 'success'
            assert response.get('message') == SUCCESS_MESSAGES['FETCHED'] \
                .format('service')
            assert new_services[0].name == data['name']

    def test__delete_a_services_succeeds(self, init_db, client):
        """Test delete a single service"""

        with DisableUniqueIdListener(Service, 'before_insert'):
            new_services = ServiceFactory.create_batch(size=3)
            service_id = new_services[0].id

            url = api.url_for(ServiceResource, service_id=service_id)
            response_object = client.delete(url)
            response = json.loads(response_object.data.decode(CHARSETS[0]))

            assert response_object.status_code == 200
            assert response.get('status') == 'success'
            assert response.get('message') == SUCCESS_MESSAGES['DELETE'] \
                .format(new_services[0].name)

    def test__get_a_service_with_invalid_id_fails(self, init_db, client):
        """Test delete a single service with invalid id"""

        url = api.url_for(ServiceResource, service_id='invalid-id')
        response_object = client.get(url)
        response = json.loads(response_object.data.decode(CHARSETS[0]))
        assert response_object.status_code == 400
        assert response.get('status') == 'error'
        assert response.get('error') == ERROR_MESSAGES['INVALID_ID']

    def test__delete_a_service_with_invalid_id_fails(self, init_db, client):
        """Test delete a single service with invalid id"""

        url = api.url_for(ServiceResource, service_id='invalid-id')
        response_object = client.delete(url)
        response = json.loads(response_object.data.decode(CHARSETS[0]))
        assert response_object.status_code == 400
        assert response.get('status') == 'error'
        assert response.get('error') == ERROR_MESSAGES['INVALID_ID']

    def test__get_a_service_with_unknown_id_fails(self, init_db, client):
        """Test delete a single service with unknown id"""

        url = api.url_for(ServiceResource, service_id='-KWhBpDWhYHZP-Pxe1Kl')
        response_object = client.get(url)
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 404
        assert response.get('status') == 'error'
        assert response.get('error') == ERROR_MESSAGES['NOT_FOUND']

    def test__delete_a_service_with_unknown_id_fails(self, init_db, client):
        """Test delete a single service with unknown id"""

        url = api.url_for(ServiceResource, service_id='-KWhBpDWhYHZP-Pxe1Kl')
        response_object = client.delete(url)
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 404
        assert response.get('status') == 'error'
        assert response.get('error') == ERROR_MESSAGES['NOT_FOUND']

    def test__post_a_service_succeeds(self, init_db, client, headers):
        """Test creating a new service"""

        data = { "name": "TEST_SERVICE" }
        url = api.url_for(ServiceListResource)
        response_object = client.post(url,
                                      headers=headers,
                                      data=json.dumps(data))
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 201
        assert response.get('status') == 'success'
        assert response.get('message') == SUCCESS_MESSAGES['CREATED'] \
            .format('service')

    def test__post_a_service_with_invalid_data_fails(self, init_db, client,
                                                     headers):
        """Test creating a new service"""

        data = { "name": " " }
        url = api.url_for(ServiceListResource)
        response_object = client.post(url,
                                      headers=headers,
                                      data=json.dumps(data))
        response = json.loads(response_object.data.decode(CHARSETS[0]))
        error = response.get('error').get('name')

        assert response_object.status_code == 400
        assert response.get('status') == 'error'
        assert error[0] == ERROR_MESSAGES['INVALID_INPUT_NAME']

    def test__post_a_role_with_duplicate_data_fails(self, init_db, client,
                                                    headers):
        """Test creating a new service"""
        new_service = ServiceFactory()

        data = { "name": new_service.name.split('_')[0] }
        url = api.url_for(ServiceListResource)
        response_object = client.post(url,
                                      headers=headers,
                                      data=json.dumps(data))
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        error = response.get('error')

        assert response_object.status_code == 409
        assert response.get('status') == 'error'
        assert error == ERROR_MESSAGES['DUPLICATES'].format('service')

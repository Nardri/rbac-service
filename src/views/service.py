"""Services Resource module"""
from flask import request

from src.dto import ServiceDto
from src.models import Service
from src.schemas import ServiceSchema
from src.utils.api_response import response
from src.utils.constants import SUCCESS_MESSAGES, ERROR_MESSAGES
from src.utils.raise_errors import raises
from src.utils.validations import validate_id
from src.views.base import BaseResource

SERVICE_NS = ServiceDto.service_ns
SERVICE_DTO = ServiceDto.service_dto
SERVICE_RESPONSE = ServiceDto.service_response


@SERVICE_NS.route('/<string:service_id>')
@SERVICE_NS.response(404, 'Service not found.')
@SERVICE_NS.param('service_id', 'The service identifier')
class ServiceResource(BaseResource):
    """Services resource"""

    model = Service
    schema = ServiceSchema()

    @SERVICE_NS.doc('Get a service')
    @validate_id
    def get(self, service_id):
        """Get a service"""

        service = self.get_object(service_id)
        serialized_service = self.schema.dump(service)
        return response(serialized_service,
                        SUCCESS_MESSAGES['FETCHED'].format('service'))

    @SERVICE_NS.doc('Delete Service')
    @SERVICE_NS.response(204, 'Service Deleted.')
    @validate_id
    def delete(self, service_id):
        """Delete a service"""

        service = self.get_object(service_id)
        deleted_service = self.model.delete(service)
        return response(
            message=SUCCESS_MESSAGES['DELETE'].format(deleted_service.name))


@SERVICE_NS.route('/')
class ServiceListResource(BaseResource):
    """Services resource"""

    model = Service
    schema = ServiceSchema()

    @SERVICE_NS.doc('list_services')
    @SERVICE_NS.marshal_list_with(SERVICE_RESPONSE)
    def get(self):
        """Get services"""

        services = self.get_queryset().all()
        serialized_roles = self.schema.dump(services, many=True)
        return response(serialized_roles,
                        SUCCESS_MESSAGES['FETCHED'].format('services'))

    @SERVICE_NS.doc('Create Role')
    @SERVICE_NS.expect(SERVICE_DTO, validate=True)
    @SERVICE_NS.marshal_with(SERVICE_RESPONSE,
                             code=201,
                             description='Service created.')
    def post(self):
        """Create a new service"""

        # get the request data in json format
        request_json = request.get_json()

        # serialize and validate the request
        service_details = self.schema.load(request_json)
        service_details['name'] = service_details['name'].strip().upper()

        service = self.model.query_(name=service_details['name']).first()
        if service:
            raises(ERROR_MESSAGES['DUPLICATES'].format('service'), 409)

        saved_service = self.model(**service_details).save()
        new_service = self.schema.dump(saved_service)

        if new_service:
            return response(new_service,
                            status_code=201,
                            object_name='service')

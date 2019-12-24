"""Data transfer object for service"""

from flask_restplus import Namespace, fields


class ServiceDto:
    """Dto class for services"""

    service_ns = Namespace('service', description='service related operation')
    service_dto = service_ns.model(
        'Services', {"name": fields.String(required=True, min=3, max=100)})

    service_model = service_ns.model(
        'ServiceModel', {
            "id": fields.String,
            "name": fields.String,
            "createdAt": fields.DateTime,
            "updatedAt": fields.DateTime,
        })

    service_response = service_ns.model(
        'ServiceResponse', {
            "status": fields.String,
            "message": fields.String,
            "data": fields.Nested(service_model)
        })

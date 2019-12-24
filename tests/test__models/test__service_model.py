"""Test model for services model"""

from src.models import Service
from src.factories import ServiceFactory
from src.schemas import ServiceSchema


class TestServiceModel:
    """Test Class for the service model"""
    def test__save_service_object_succeeds(self, init_db):
        """Test for the save method"""

        service = ServiceFactory()
        saved_service = service.save()
        assert saved_service.name == service.name

    def test__get_service_succeeds(self, init_db):
        """Test get services"""

        services = ServiceFactory.create_batch(size=10)
        db_services = Service.query_()

        schema = ServiceSchema(many=True)
        serialized_services = schema.dump(db_services)

        assert len(serialized_services) == 10
        assert serialized_services[0].get('name') == services[0].name

    def test__service_repr(self, init_db):
        """Test the string representation for service"""

        service = ServiceFactory()
        service_string = f'<Service {service.name}>'

        assert str(service) == service_string

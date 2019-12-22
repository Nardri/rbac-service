"""Service factory module"""

import factory
from faker import Faker
from faker.providers import lorem

from src.factories import BaseFactory
from src.models.service import Service
from app import database as db

faker = Faker()
faker.add_provider(lorem)


class ServiceFactory(BaseFactory):
    """Service factory"""

    name = factory.Sequence(lambda o: f'{faker.word().upper()}_SERVICE')
    active = factory.Iterator([False, True])

    class Meta:
        """Service Meta class"""

        model = Service
        sqlalchemy_session = db.session

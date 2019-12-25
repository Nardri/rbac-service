"""Factory module for the role model"""

import factory
from src.models.role import Role
from src.factories import BaseFactory

from app import database as db


class RoleFactory(BaseFactory):
    """Role Factory"""

    name = factory.Sequence(lambda n: f'role{n}')
    is_default = factory.Iterator([False, True])

    class Meta:
        """Role factory meta class"""

        model = Role
        sqlalchemy_session = db.session


class RoleWithPermissionFactory(RoleFactory):
    """Role with permissions factory"""
    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        """post generations"""
        import random
        from src.factories import PermissionFactory

        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            PermissionFactory(role=self, type=extracted)

        else:
            number_of_units = random.randint(1, 10)
            for n in range(number_of_units):
                PermissionFactory(role=self)

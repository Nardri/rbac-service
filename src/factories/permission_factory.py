"""Permission factory module"""

import factory
from src.factories import BaseFactory
from src.models.permission import Permission, PermissionType
from app import database as db


class PermissionFactory(BaseFactory):
    """Permissions factory"""

    type = factory.Iterator([PermissionType.All, PermissionType.NONE])
    active = factory.Iterator([False, True])
    service_id = factory.RelatedFactory('src.factories.ServiceFactory')
    service = factory.SubFactory('src.factories.ServiceFactory')
    role = factory.SubFactory('src.factories.RoleFactory')

    class Meta:
        """Permissions Meta class"""

        model = Permission
        sqlalchemy_session = db.session

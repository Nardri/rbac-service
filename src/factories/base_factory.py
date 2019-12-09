"""Base factory"""

import factory
from src.utils.date_time import date_time
from src.utils.push_id import PushID

push_id = PushID()


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Base factory for all factories"""

    __abstract__ = True

    id = factory.LazyFunction(push_id.next_id)

    created_at = factory.LazyFunction(date_time.time)
    updated_at = factory.LazyFunction(date_time.time)

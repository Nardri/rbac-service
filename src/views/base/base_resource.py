"""Base resource"""

from flask_restplus import Resource

from src.utils.constants import ERROR_MESSAGES
from src.utils.raise_errors import raises


class BaseResource(Resource):
    """Base Resource"""

    __abstract__ = True

    # instantiate the role schema
    schema = None
    model = None

    @classmethod
    def get_queryset(cls):
        """Returns model queryset."""

        return cls.model.query

    @classmethod
    def get_object(cls, id_):
        """ Returns a single model object."""

        object = cls.get_queryset().get(id_)
        if not object:
            raises(ERROR_MESSAGES['NOT_FOUND'], 404)
        return object

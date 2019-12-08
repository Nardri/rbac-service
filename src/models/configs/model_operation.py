"""Common model operations"""

from .database import database as db


class ModelOperation(object):
    """Model operation"""

    def save(self):
        """Save to the database."""

        db.session.add(self)
        db.session.commit()
        return self

    def update_(self, **kwargs):
        """Update entries.
        Args:
            **kwargs: kwargs to update
        Returns:
            object: Model Instance
        """
        for field, value in kwargs.items():
            setattr(self, field, value)
        db.session.commit()

        return self

    @classmethod
    def query_(cls, **kwargs):
        """
        Args:
            **kwargs:
        Returns:
            Object :
        """
        if not kwargs:
            instance = cls.query.filter_by(deleted=False).order_by(
                cls.created_at)
        else:
            instance = cls.query.filter_by(**kwargs)
        return instance

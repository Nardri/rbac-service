"""Permission Model"""
import enum

from src.models.base.base_model import BaseModel
from src.models.configs.database import database as db


class PermissionType(enum.Enum):
    """
    Permission Enum
    """
    All = 0
    READ = 1
    WRITE = 2
    EDIT = 3
    DELETE = 4
    NONE = 5


class Permission(BaseModel):
    """Permission table"""

    # table name
    __tablename__ = 'permissions'

    type = db.Column(db.Enum(PermissionType), default=PermissionType.NONE)
    active = db.Column(db.Boolean, default=False)
    service_id = db.Column(db.String(36),
                           db.ForeignKey('services.id', ondelete="CASCADE"),
                           nullable=False)
    role_id = db.Column(db.String(36),
                        db.ForeignKey('roles.id', ondelete="CASCADE"),
                        nullable=False)

    def __repr__(self):
        return '<Permission {} for {}>'.format(self.type, self.service.name)

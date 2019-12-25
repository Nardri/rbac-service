"""Permission Model"""
import enum

from src.models.base.base_model import BaseModel
from src.models.configs.database import database as db


class PermissionType(enum.Enum):
    """
    Permission Enum
    """
    FULL_ACCESS = 'all'
    READ = 'read'
    WRITE = 'write'
    EDIT = 'edit'
    DELETE = 'delete'
    NONE = 'none'

    @classmethod
    def get_enum_member_names(cls):
        """Get enum member names"""
        return [name for name, _ in cls.__members__.items()]

    @classmethod
    def get_enum_member_values(cls):
        """Get enum members"""
        return [member.value for _, member in cls.__members__.items()]

    @classmethod
    def get_enum_members(cls):
        """Get enum members"""
        return [member for _, member in cls.__members__.items()]


class Permission(BaseModel):
    """Permission table"""

    # table name
    __tablename__ = 'permissions'

    type = db.Column(db.Enum(PermissionType), default=PermissionType.NONE)
    service_id = db.Column(db.String(36),
                           db.ForeignKey('services.id', ondelete="CASCADE"),
                           nullable=False)
    role_id = db.Column(db.String(36),
                        db.ForeignKey('roles.id', ondelete="CASCADE"),
                        nullable=False)

    def __repr__(self):
        return '<Permission {} for {}>'.format(self.type, self.service.name)

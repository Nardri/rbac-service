"""Test model for permission model"""
from src.models.permission import PermissionType
from src.models import Permission
from src.factories import PermissionFactory
from src.schemas import PermissionSchema


class TestPermissionModel:
    """Test Class for the permission model"""
    def test__save_permission_object_succeeds(self, init_db):
        """Test for the save method"""

        permission = PermissionFactory()
        saved_permission = permission.save()
        assert saved_permission.type == permission.type

    def test__get_permission_succeeds(self, init_db):
        """Test get permissions"""

        permissions = PermissionFactory.create_batch(size=10)
        db_permission = Permission.query_()

        schema = PermissionSchema(many=True)
        serialized_roles = schema.dump(db_permission)

        assert len(serialized_roles) == 10
        assert serialized_roles[0].get('type') == permissions[0].type.name

    def test__permission_repr(self, init_db):
        """Test the string representation for permission"""

        permission = PermissionFactory()
        permission_string = f'<Permission {permission.type} for ' \
                            f'{permission.service.name}>'
        assert str(permission) == permission_string

    def test__get_permission_enum_members(self, init_db):
        """Test the string representation for permission"""

        members = PermissionType.get_enum_members()
        name = PermissionType.get_enum_member_names()
        values = PermissionType.get_enum_member_values()

        assert isinstance(members, list)
        assert isinstance(name, list)
        assert isinstance(values, list)

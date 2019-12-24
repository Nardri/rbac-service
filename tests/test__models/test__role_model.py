"""Test model for roles model"""

from src.models.role import Role
from src.factories import RoleWithPermissionFactory
from src.schemas.role_schema import RoleSchema


class TestRoleModel:
    """Test Class for the roles model"""
    def test__save_role_object_succeeds(self, init_db):
        """Test for the save method"""

        role = RoleWithPermissionFactory()
        saved_role = role.save()
        assert saved_role.name == role.name

    def test__get_role_succeeds(self, init_db):
        """Test get roles"""

        roles = RoleWithPermissionFactory.create_batch(size=10)
        db_role = Role.query_()

        schema = RoleSchema(many=True)
        serialized_roles = schema.dump(db_role)

        assert len(serialized_roles) == 10
        assert serialized_roles[0].get('name') == roles[0].name

    def test__update_role_succeeds(self, init_db):
        """Test Update role method"""

        role = RoleWithPermissionFactory.create(name='before_update',
                                                permissions='None')
        updated_role = role.update_(name='updated')

        assert updated_role.name == 'updated'

    def test__role_repr(self, init_db):
        """Test the string representation for role"""

        role = RoleWithPermissionFactory()
        role_string = f'<Role {role.name}>'

        assert str(role) == role_string

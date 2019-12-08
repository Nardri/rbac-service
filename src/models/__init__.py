"""Models"""

from sqlalchemy import event

from src.utils.push_id import PushID
from src.models.role import Role
from src.models.permission import Permission
from src.models.service import Service


def generate_unique_id(mapper, connection, target):
    """Generates a firebase fancy unique Id
    Args:
            mapper (obj): The current model class
            connection (obj): The current database connection
            target (obj): The current model instance
    Returns:
                    None
    """
    push_id = PushID()
    target.id = push_id.next_id()


tables = [
    Role,
    Permission,
    Service
]


for table in tables:
    event.listen(table, 'before_insert', generate_unique_id)

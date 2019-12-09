"""Base model"""

# local imports
from src.models.configs.database import database as db
from src.models.configs.model_operation import ModelOperationsMixin

# utilities
from src.utils.date_time import date_time


class BaseModel(db.Model, ModelOperationsMixin):
    """Base model"""

    __abstract__ = True

    id = db.Column(db.String(36), unique=True, primary_key=True)

    created_at = db.Column(db.DateTime, default=date_time.time())
    updated_at = db.Column(db.DateTime, onupdate=date_time.time())

"""Role Model"""
from src.models.base.base_model import BaseModel
from src.models.configs.database import database as db


class Role(BaseModel):
    """Role table"""

    # table name
    __tablename__ = 'roles'

    name = db.Column(db.String(80), nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    permissions = db.relationship('Permission', backref='role', lazy=True)

    def __repr__(self):
        return '<Role {}>'.format(self.name)

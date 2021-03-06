"""Service Model"""
from src.models.base.base_model import BaseModel
from src.models.configs.database import database as db


class Service(BaseModel):
    """Service table"""

    # table name
    __tablename__ = 'services'

    name = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    permissions = db.relationship('Permission',
                                  lazy=True,
                                  backref=db.backref('service', lazy=True))

    def __repr__(self):
        return '<Service {}>'.format(self.name)

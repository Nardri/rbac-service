"""Database setup"""

# Third party library
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# initialization of the database and migration
database = SQLAlchemy()
migrate = Migrate()

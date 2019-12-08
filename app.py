"""Application main file"""

# Third party library
from flask import Flask, jsonify
from flask_restplus import Api

# local import
from config import app_config
from src import api_blueprint
from src.models.configs.database import (database, migrate)

# initialize RestPlus with the API blueprint
api = Api(api_blueprint, doc='/doc/',
          description="Documentation for the RBAC service")


def register_blueprints(application):
    """Registers all blueprints
    Args:
        application (obj): Application instance
    Returns:
        None
    """

    application.register_blueprint(api_blueprint)


def create_app(env):
    """Create the flask application instance
    Args:
        env (string): The environment
    Returns:
        Object: Flask instance
    """

    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[env])

    # register the blueprint
    register_blueprints(app)

    # import models
    import src.models
    
    # Import views
    import src.views

    # Bind Database to the app instance
    database.init_app(app)

    # Bind migrate to the application instance
    migrate.init_app(app, database)

    @app.route('/', methods=['GET'])
    def health():
        """Index Route"""
        return jsonify(
            data={
                "status": 'success',
                "message": 'Role Based Access Control Service.'
            },
        )

    return app

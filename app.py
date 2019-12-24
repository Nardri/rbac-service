"""Application main file"""

# Third party library
from flask import Flask, jsonify
from flask_restplus import Api

# local import
from config import app_config
from src import rbac_blueprint
from src.models.configs.database import (database, migrate)
from src.utils.application_error import ApplicationError
from src.views.role import ROLE_NS
from src.views.service import SERVICE_NS

# initialize RestPlus with the API blueprint
api = Api(rbac_blueprint,
          doc='/doc/',
          description="Documentation for the RBAC service")

api.add_namespace(ROLE_NS)
api.add_namespace(SERVICE_NS)


def register_blueprints(application):
    """Registers all blueprints
    Args:
        application (obj): Application instance
    Returns:
        None
    """

    application.register_blueprint(rbac_blueprint)


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
        return jsonify(data={
            "status": 'success',
            "message": 'Role Based Access Control Service.'
        }, )

    return app


@rbac_blueprint.errorhandler(ApplicationError)
def handle_exceptions(err):
    """Custom Application Error handler."""

    return err.to_dict()

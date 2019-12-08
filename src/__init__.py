"""Blueprint module"""

from flask import Blueprint

# instantiating the blue print
api_blueprint = Blueprint('rbac-service', __name__, url_prefix='/api/v1')

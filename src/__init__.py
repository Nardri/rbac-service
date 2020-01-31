"""Blueprint module"""

from flask import Blueprint

# instantiating the blue print
rbac_blueprint = Blueprint('rbac-service', __name__, url_prefix='/v1')

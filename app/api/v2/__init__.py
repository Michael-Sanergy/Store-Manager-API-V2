from flask import Blueprint
from flask_restplus import Api

# Local import
from .views import namespace_1 as n1

# create a blueprint
app_version2 = Blueprint("v2", __name__, url_prefix="/api/v2")
api_version2 = Api(app_version2)

# Add namespaces
api_version2.add_namespace(n1, path='/auth/signup')

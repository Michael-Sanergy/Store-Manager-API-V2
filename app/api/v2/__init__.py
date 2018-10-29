from flask import Blueprint
from flask_restplus import Api

# Local import
from .views import namespace_1 as n1
from .views import namespace_2 as n2

# create a blueprint
app_version2 = Blueprint("v2", __name__, url_prefix="/api/v2")
api_version2 = Api(app_version2)

# Add namespaces
api_version2.add_namespace(n1, path='/auth/signup')
api_version2.add_namespace(n2, path='/auth/login')

from flask import Blueprint
from flask_restplus import Api
from .utils import authorizations

# Local import
from .views import namespace_1 as n1
from .views import namespace_2 as n2
from .views import namespace_3 as n3
from .views import namespace_4 as n4

# create a blueprint
app_version2 = Blueprint("v2", __name__, url_prefix="/api/v2")
api_version2 = Api(app_version2, authorizations=authorizations)

# Add namespaces
api_version2.add_namespace(n1, path='/auth/signup')
api_version2.add_namespace(n2, path='/auth/login')
api_version2.add_namespace(n3, path='/products')
api_version2.add_namespace(n4, path='/sales')

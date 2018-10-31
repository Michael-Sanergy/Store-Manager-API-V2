from flask import Flask
from flask_jwt_extended import JWTManager

# Local import
from instance.config import app_config
from .api.v2.database import create_tables


def create_app(config_name):
    """Create an instance of Flask and load with environment variables"""

    app = Flask(__name__, instance_relative_config=True)
    JWTManager(app)

    # Create database tables
    create_tables()

    # Remove trailing slash in url
    app.url_map.strict_slashes = False

    # Import blueprint we created
    from .api.v2 import app_version2

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # Register blueprint we created
    app.register_blueprint(app_version2)

    return app

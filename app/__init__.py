from flask import Flask

# Local import
from instance.config import app_config


def create_app(config_name):
    """Create an instance of Flask and load with environment variables"""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    return app

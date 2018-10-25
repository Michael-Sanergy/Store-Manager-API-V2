import os

# Local import
from app import create_app

# Get environment settings Flask should use
config_name = os.getenv('FLASK_ENV')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()

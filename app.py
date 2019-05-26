from flask import Flask
from flask_nav import Nav

app = Flask(__name__, static_url_path='')

# Parse Flask configuration
from config import CONFIGURATION
app.config.from_object(CONFIGURATION)

# Function for create navigation menu
from create_header import create_header
create_header(Nav(app), app)

#  Auth Manager
from modules.AuthManager.app import auth__module
app.register_blueprint(auth__module)

# API
from modules.api.app import api_module
app.register_blueprint(api_module, url_prefix='/api')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
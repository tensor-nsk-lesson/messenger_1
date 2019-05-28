from flask import Flask
from flask_nav import Nav

app = Flask(__name__, static_url_path='')

# Parse Flask configuration
from config import CONFIGURATION
app.config.from_object(CONFIGURATION)

#  Auth Manager
from AuthManager.routes import auth_module
app.register_blueprint(auth_module)

#  Profile Manager
from ProfileManager.routes import profile_module
app.register_blueprint(profile_module)

#  Messages Manager
from MessagesManager.routes import messages_module
app.register_blueprint(messages_module)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
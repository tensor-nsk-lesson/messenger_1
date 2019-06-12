from flask import Flask

app = Flask(__name__, static_url_path='')


#  Mail Manager
from modules.AuthManager.MailManager.routes import mail_module
app.register_blueprint(mail_module)

#  Auth Manager
from modules.AuthManager.routes import auth_module
app.register_blueprint(auth_module)

#  Profile Manager
from modules.ProfileManager.routes import profile_module
app.register_blueprint(profile_module, url_prefix='/profile')

#  Chat Manager
from modules.ChatManager.routes import messages_module
app.register_blueprint(messages_module, url_prefix='/chat')

# Parse Flask configuration
app.config.from_pyfile('config.ini')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
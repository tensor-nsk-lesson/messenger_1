from flask import Flask
from messenger_1.src import app

#  Mail Manager
from modules.Routes.MailManager import mail_module
app.register_blueprint(mail_module)

#  Auth Manager
from modules.Routes.AuthManager import auth_module
app.register_blueprint(auth_module)

#  Profile Manager
from modules.Routes.ProfileManager import profile_module
app.register_blueprint(profile_module, url_prefix='/profile')

#  Chat Manager
from modules.Routes.ChatManager import messages_module
app.register_blueprint(messages_module, url_prefix='/chat')

# Parse Flask configuration
app.config.from_pyfile('config.ini')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
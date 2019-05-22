from flask import Flask
from flask_nav import Nav

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'uzE7lSw8Ch7X4aB81E22Z6Nh'

# Function for create navigation menu
from api.create_header import create_header
create_header(Nav(app), app)

#  Auth Manager
from modules.AuthManager.app import auth_blueprint
app.register_blueprint(auth_blueprint)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
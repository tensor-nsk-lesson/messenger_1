from flask_bootstrap import Bootstrap
from flask_nav.elements import Navbar, Subgroup, View
from routes import index


def create_header(nav, app):
    nav.register_element('navbar', Navbar(
        View('MEVO', 'index'),
        View('Login', 'auth.hLogin'),
        View('Register', 'auth.hRegister'),
        Subgroup('Routes',
            View('Reset Password', 'auth.hResetPW')
    )))

    Bootstrap(app)
    nav.init_app(app)

from flask_bootstrap import Bootstrap
from flask_nav.elements import Navbar, Subgroup, View
from routes import index


def create_header(nav, app):
    nav.register_element('navbar', Navbar(
        View('MEVO', 'index'),
        View('Войти', 'auth.hLogin'),
        View('Зарегистрироваться', 'auth.hRegister'),
        Subgroup('Роуты',
            View('Сбросить пароль', 'auth.hResetPW')
    )))

    Bootstrap(app)
    nav.init_app(app)

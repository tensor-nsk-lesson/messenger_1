from flask import Blueprint, render_template
from modules.AuthManager.forms import fRegistration, fLogin, fResetPW

auth_blueprint = Blueprint('auth', __name__, template_folder='templates/AuthManager')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def hRegister():
    form = fRegistration()
    return render_template('AuthManager/register.html', title='MEVO | Регистрация', form=form)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def hLogin():
    form = fLogin()
    return render_template('AuthManager/login.html', title='MEVO | Авторизация', form=form)


@auth_blueprint.route('/reset-password', methods=['GET', 'POST'])
def hResetPW():
    form = fResetPW()
    return render_template('AuthManager/reset.html', title='MEVO | Сброс пароля', form=form)

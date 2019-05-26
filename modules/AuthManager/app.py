from flask import Blueprint, render_template, request, session
from modules.AuthManager.forms import fRegistration, fLogin, fResetPW
from modules.AuthManager.content_handler import FormContainHandler
from db_handle import db_isValidUser, db_addUser
from hashlib import sha256

auth_blueprint = Blueprint('auth', __name__, template_folder='templates/AuthManager')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def hRegister():
    form = fRegistration()
    if request.method == 'POST':
        data = FormContainHandler(request.form.to_dict())
        if not db_isValidUser(data):
            db_addUser(data)
            print('Регистрация прошла успешно')
        else: print('Регистрация не удалась! :(')

    return render_template('AuthManager/register.html', title='MEVO | Регистрация', form=form)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def hLogin():
    form = fLogin()
    if request.method == 'POST':
        data = FormContainHandler(request.form.to_dict())

        data.update({'password': sha256(data['password'].encode())})  # Хешируем введённый пользователем пароль
        if db_isValidUser(data) and not session['log_in']:
            session['log_in'] = True
            print('Авторизация прошла успешно')
    return render_template('AuthManager/login.html', title='MEVO | Авторизация', form=form)


@auth_blueprint.route('/reset-password/', methods=['GET', 'POST'])
def hResetPW():
    form = fResetPW()
    if request.method == 'POST':
        data = request.form.to_dict()

    return render_template('AuthManager/reset.html', title='MEVO | Сброс пароля', form=form)

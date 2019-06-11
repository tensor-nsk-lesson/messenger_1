from flask import Blueprint, request, redirect, jsonify, make_response, abort, url_for
from modules.ProfileManager.api.db_methods import db_isAuthDataValid, db_addProfile, db_getUserIDbyEmail, db_getUserIDbyLogin
from modules.ProfileManager.api.db_methods import db_setLastVisit
from modules.ProfileManager.api.functions import isProfileBlocked, isProfileDeleted
from modules.ProfileManager.api.db_methods import db_isProfileExists, db_updateProfileInfo
from modules.AuthManager.SessionControl.app import initRedis_db
from modules.json_validator import json_validate
from modules.json_schemas import login_schema, register_schema, email_schema
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from src.app import app
from hashlib import sha256
from random import randint
import uuid
import time
import re

auth_module = Blueprint('auth', __name__)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@auth_module.route('/register', methods=['GET', 'POST'])
def hRegister():
    if request.method == 'POST':
        data = json_validate(request.data, register_schema)

        if not data:
            return abort(400)

        if not data['login'] \
                or not data['password'] \
                or not data['first_name'] \
                or not data['second_name'] \
                or not data['email']:
            return jsonify({'status': 0, 'message': 'Заполнены не все данные'})

        if db_isProfileExists(data):
            return jsonify({'status': 0, 'message': 'Аккаунт с таким логином уже существует'})

        data.update({'password': sha256(data['password'].encode()).hexdigest()})

        return jsonify(db_addProfile(data))


@auth_module.route('/', methods=['GET', 'POST'])
@auth_module.route('/login', methods=['GET', 'POST'])
def hLogin():
    r = initRedis_db()
    if request.method == 'POST':
        if request.cookies['SESSION']:
            UUID = request.cookies['SESSION']
            if r.get(UUID):
                return jsonify({'status': 0, 'message': 'Вы уже авторизованы'})

        data = json_validate(request.data, login_schema)
        if not data:
            return abort(400)
        if not data['login'] or not data['password']:
            return jsonify({'status': 0, 'message': 'Заполнены не все данные'})

        data.update({'password': sha256(data['password'].encode()).hexdigest()})

        if not db_isAuthDataValid(data):
            return jsonify({'status': 0, 'message': 'Неправильный логин/пароль'})

        user_id = db_getUserIDbyLogin(data)
        if not user_id:
            return jsonify({'status': 0, 'message': 'Такого аккаунта не существует'})

        if isProfileBlocked(user_id):
            return jsonify({'status': 0, 'message': 'Данный аккаунт заблокирован'})
        elif isProfileDeleted(user_id):
            return jsonify({'status': 0, 'message': 'Данный аккаунт удалён'})

        db_setLastVisit(user_id)

        salt = ''.join([chr(randint(97, 122)) for _ in range(32)])
        generate_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(user_id + time.time()) + salt))

        #return jsonify(db_getProfileInfo(user_id))
        r.set(generate_uuid, user_id, ex=1000)
        response = make_response(redirect('/profile/{}'.format(user_id)))
        response.set_cookie('SESSION', bytes(generate_uuid, 'utf-8'))
        return response


# TODO: Сделать валидацию JSON'а от пользователя
@auth_module.route('/logout', methods=['GET', 'POST'])
def logout():
    r = initRedis_db()
    if not request.cookies.get('SESSION'):
        jsonify({'status': 0, 'message': 'Вы не авторизованы'})

    UUID = request.cookies.get('SESSION')
    r.delete(UUID)

    return jsonify({'status': 1})


# TODO: Сделать валидацию JSON'а от пользователя

@auth_module.route('/reset-password')
def resetPW_request():
    r = initRedis_db()
    global userid

    if request.method == 'GET':
        email = request.args.get('email')
        if not email:
            return jsonify({'status': 0, 'message': 'Требуется параметр с email'})

        if ''.join(re.findall(r'^[0-9A-z-_]+@[0-9A-z-_]+.[0-9A-z]+$', email)) != email:
            return jsonify({'status': 0, 'message': 'Неправильный формат email\'а'})

        mail = Mail(app)
        token = s.dumps(email, salt=app.config['SECRET_KEY'])
        msg = Message('Confirm Email', sender='mevomsngr@yandex.ru', recipients=[email])
        link = url_for('resetPW', token=token, _external=True)
        msg.body = 'Ссылка для сброса пароля: {}. Если вы не отправляли запрос на сброс пароля, то просто проигнорируйте это сообщение.'.format(
            link)
        mail.send(msg)
        userid = db_getUserIDbyEmail(email)
        # data.update({'password': sha256(data['password'].encode())})  # Хешируем введённый пользователем пароль
        return jsonify({'status': 1})



@auth_module.route('/reset-password/<token>', methods=['POST'])
def resetPW(token):
    if request.method == 'POST':
        data = json_validate(request.json, email_schema)
        if not data:
            return abort(400)

        if not data['email']:
            return jsonify({'status': 0, 'message': 'Требуется email'})

        if isTokenExpired(token):
            return jsonify({'status': 0, 'message': 'Токен просрочился'})

        r.delete(userid)
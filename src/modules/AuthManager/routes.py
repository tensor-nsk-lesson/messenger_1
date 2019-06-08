from flask import Blueprint, request, redirect, jsonify, make_response, abort
from modules.ProfileManager.api.db_methods import db_isAuthDataValid, db_addProfile, db_getProfileInfo, db_getUserID
from modules.ProfileManager.api.db_methods import db_setLastVisit
from modules.ProfileManager.api.functions import isProfileBlocked, isProfileDeleted
from modules.ProfileManager.api.db_methods import db_isProfileExists
from modules.AuthManager.SessionControl.app import initRedis_db
from modules.json_validator import json_validate
from modules.json_schemas import login_schema, register_schema
from hashlib import sha256
from random import randint
import uuid
import json
import re
import time

auth_module = Blueprint('auth', __name__)


@auth_module.route('/register', methods=['POST'])
def hRegister():
    if request.method == 'POST':
        data = json_validate(request.data, register_schema)

        if not data:
            return abort(400)

        if not data['login'] or not data['password'] or not data['first_name'] or not data['second_name']:
            return jsonify({'status': 0, 'message': 'Заполнены не все данные'})

        if db_isProfileExists(data):
            return jsonify({'status': 0, 'message': 'Аккаунт с таким логином уже существует'})

        data.update({'password': sha256(data['password'].encode()).hexdigest()})

        return jsonify(db_addProfile(data))


@auth_module.route('/', methods=['POST'])
@auth_module.route('/login', methods=['POST'])
def hLogin():
    r = initRedis_db()
    if request.method == 'POST':
        data = json_validate(request.data, login_schema)
        if not data:
            return abort(400)
        if not data['login'] or not data['password']:
            return jsonify({'status': 0, 'message': 'Заполнены не все данные'})

        # if ''.join(re.findall(r'\w+', data['login'])) != data['login']:
        #     return jsonify({'status': 0, 'message': 'Логин должно состоять только из букв и цифр'})
        #
        # if ''.join(re.findall(r'\w+', data['password'])) != data['password']:
        #     return jsonify({'status': 0, 'message': 'Пароль должно состоять только из букв и цифр'})

        data.update({'password': sha256(data['password'].encode()).hexdigest()})

        if not db_isAuthDataValid(data):
            return jsonify({'status': 0, 'message': 'Неправильный логин/пароль'})

        user_id = db_getUserID(data)
        if isProfileBlocked(user_id):
            return jsonify({'status': 0, 'message': 'Данный аккаунт заблокирован'})
        elif isProfileDeleted(user_id):
            return jsonify({'status': 0, 'message': 'Данный аккаунт удалён'})

        db_setLastVisit(user_id)

        salt = ''.join([chr(randint(97, 122)) for _ in range(32)])
        generate_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(user_id + time.time()) + salt))

        #return jsonify(db_getProfileInfo(user_id))
        r.set(generate_uuid, user_id)
        response = make_response(redirect('/profile/{}'.format(user_id)))
        response.set_cookie('SESSION', bytes(generate_uuid, 'utf-8'))
        return response


# TODO: Сделать валидацию JSON'а от пользователя
@auth_module.route('/logout', methods=['GET', 'POST'])
def logout():
    r = initRedis_db()
    UUID = request.cookies.get('SESSION')
    r.delete(UUID)
    return jsonify({'status': 1})


# TODO: Сделать валидацию JSON'а от пользователя
@auth_module.route('/reset-password/', methods=['GET', 'POST'])
def resetPW():
    r = initRedis_db()
    if request.method == 'POST':
        UUID = request.cookies.get('SESSION')
        r.delete(UUID)
        # data.update({'password': sha256(data['password'].encode())})  # Хешируем введённый пользователем пароль
        return redirect('index')

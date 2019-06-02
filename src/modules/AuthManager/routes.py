from flask import Blueprint, request, redirect, jsonify, abort
from modules.ProfileManager.api.db_methods import db_isAuthDataValid, db_addProfile, db_getProfileInfo, db_getUserID, db_setLastVisit
from modules.ProfileManager.api.db_methods import db_isProfileExists
from modules.SessionControl.app import initRedis_db, generateSession
#from flask_expects_json import expects_json
from hashlib import sha256
from modules.json_schemas import login_schema, register_schema
import jsonschema
import json


auth_module = Blueprint('auth', __name__)

@auth_module.route('/register', methods=['GET', 'POST'])
def hRegister():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            jsonschema.validate(data, register_schema)
        except (jsonschema.exceptions.ValidationError, json.decoder.JSONDecodeError):
            return {'status': -1, 'message': 'Найдены ошибки в JSON\'е'}

        data.update({'password': sha256(data['password'].encode()).hexdigest()})

        if db_isProfileExists(data):
            return jsonify({'status': 0, 'message': 'Аккаунт с таким логином уже зарегистрирован'})

        return jsonify(db_addProfile(data))


@auth_module.route('/', methods=['GET', 'POST'])
@auth_module.route('/login', methods=['GET', 'POST'])
def hLogin():
    r = initRedis_db()
    if request.method == 'POST':
        try:
            try:
                data = json.loads(request.data)
                jsonschema.validate(data, login_schema)
            except (jsonschema.exceptions.ValidationError, json.decoder.JSONDecodeError):
                return {'status': -1, 'message': 'Найдены ошибки в запросе'}

            if not data:
                return jsonify({'status': 0, 'message': 'Требуются логин и пароль для авторизации'})

            if not data['login'] and data['password']:
                return jsonify({'status': 0, 'message': 'Требуются логин и пароль для авторизации'})

            if not data['login']:
                return jsonify({'status': 0, 'message': 'Требуется логин для авторизации'})

            if not data['password']:
                return jsonify({'status': 0, 'message': 'Требуется пароль для авторизации'})

            data.update({'password': sha256(data['password'].encode()).hexdigest()})

            if not db_isAuthDataValid(data):
                return jsonify({'status': 0, 'message': 'Неправильный логин/пароль'})

            user_id = db_getUserID(data)
            if db_getProfileInfo(user_id)['is_blocked']:
                return jsonify({'status': 0, 'message': 'Аккаунт заблокирован'})
        except Exception as err:
            print('[ERROR!]', err)

        db_setLastVisit(user_id)
        generateSession(user_id, r)
        return jsonify(db_getProfileInfo(user_id))


# TODO: Сделать валидацию JSON'а от пользователя
@auth_module.route('/logout', methods=['GET', 'POST'])
def logout():
    data = json.loads(request.data)
    r = initRedis_db()
    r.delete(db_getUserID(data))
    return jsonify({'status': 1})


# TODO: Сделать валидацию JSON'а от пользователя
@auth_module.route('/reset-password/', methods=['GET', 'POST'])
def hResetPW():
    r = initRedis_db()
    if request.method == 'POST':
        data = json.loads(request.data)
        r.delete(db_getUserID(data))
        #data.update({'password': sha256(data['password'].encode())})  # Хешируем введённый пользователем пароль
        return redirect('index')

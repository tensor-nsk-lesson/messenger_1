from flask import Blueprint, request, redirect, jsonify, make_response
from api.db_methods import db_isAuthDataValid, db_addProfile, db_getProfileInfo, db_getUserID, db_setLastVisit
from api.db_methods import db_delProfile, db_isProfileExists, db_isProfileBlocked
from SessionControl.app import initRedis_db, generateSession
from flask_expects_json import expects_json
from json_schemas import login_schema, register_schema
from hashlib import sha256
import json


auth_module = Blueprint('auth', __name__)

@auth_module.route('/register', methods=['GET', 'POST'])
@expects_json(register_schema)
def hRegister():
    if request.method == 'POST':
        data = json.loads(request.data)
        data.update({'password': sha256(data['password'].encode()).hexdigest()})

        if db_isProfileExists(data):
            return jsonify({'status': 0, 'message': 'Аккаунт с таким логином уже зарегистрирован'})
        return jsonify(db_addProfile(data))


@auth_module.route('/', methods=['GET', 'POST'])
@auth_module.route('/login', methods=['GET', 'POST'])
@expects_json(login_schema)
def hLogin():
    r = initRedis_db()
    if request.method == 'POST':
        data = json.loads(request.data)
        if not data:
            return jsonify({'status': 0, 'message': 'Требуются логин и пароль для авторизации'})

        data.update({'password': sha256(data['password'].encode()).hexdigest()})

        if not db_isAuthDataValid(data):
            return jsonify({'status': 0, 'message': 'Неправильный логин/пароль'})

        user_id = db_getUserID(data)
        if db_getProfileInfo(user_id)['is_blocked']:
            return jsonify({'status': 0, 'message': 'Аккаунт заблокирован'})

        db_setLastVisit(user_id)
        generateSession(user_id, r)
        return jsonify(db_getProfileInfo(user_id))



@auth_module.route('/logout', methods=['GET', 'POST'])
def logout():
    data = json.loads(request.data)
    r = initRedis_db()
    r.delete(db_getProfileInfo(data))
    return redirect('index')


@auth_module.route('/reset-password/', methods=['GET', 'POST'])
def hResetPW():
    r = initRedis_db()
    if request.method == 'POST':
        data = json.loads(request.data)
        r.delete(db_getUserID(data))
        #data.update({'password': sha256(data['password'].encode())})  # Хешируем введённый пользователем пароль
        return redirect('index')

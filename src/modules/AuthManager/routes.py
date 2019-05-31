from flask import Blueprint, request, redirect, jsonify, make_response
from api.users import db_isProfileValid, db_addProfile, db_getProfileInfo, db_getUserID, db_setLastVisit
from hashlib import sha256
from SessionControl.app import initRedis_db, generateSession
import json


auth_module = Blueprint('auth', __name__)


@auth_module.route('/register', methods=['GET', 'POST'])
def hRegister():
    r = initRedis_db()
    if request.method == 'POST':
        data = json.loads(request.data)
        data.update({'password': sha256(data['password'].encode()).hexdigest()})
        # if not db_isProfileValid(data):
        #     r.set(db_getProfileInfo(data)) # На вход подаётся словарь с ID пользователя.

    return jsonify(db_addProfile(data))


@auth_module.route('/', methods=['GET', 'POST'])
@auth_module.route('/login', methods=['GET', 'POST'])
def hLogin():
    r = initRedis_db()
    if request.method == 'POST':
        try: # Пробуем перевести введёный словарь пользователя в json.
            data = json.loads(request.data)
            if not data:
                return {'status': 0, 'message': 'Требуются логин и пароль для авторизации'}

            data.update({'password': sha256(data['password'].encode()).hexdigest()})
            user_id = db_getUserID(data)

            if db_isProfileValid(data):  #
                db_setLastVisit(user_id)
                generateSession(user_id, r)
                return jsonify(db_getProfileInfo(user_id))
        except Exception as err: # Если не смогли, то ничего не делаем.
            print(err)


@auth_module.route('/logout')
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
        r.delete(db_getProfileInfo(data))
        #data.update({'password': sha256(data['password'].encode())})  # Хешируем введённый пользователем пароль
    return redirect('index')

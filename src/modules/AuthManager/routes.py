from flask import Blueprint, request, redirect, jsonify
from api.users import db_isProfileValid, db_addProfile, db_getProfileInfo, db_getUserID
from hashlib import sha256
from SessionControl.app import initRedis_db
import time
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
    user_id = 0
    if request.method == 'POST':
        data = json.loads(request.data)
        user_id = db_getUserID(data)
        if db_isProfileValid(data):  # На вход подаётся словарь с данными пользователя. Возвращается его ID
            r.set(user_id, sha256(data['login'] + str(time.time())))
    return jsonify(db_getProfileInfo(user_id))


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

from flask import Blueprint, request, redirect
from api.users import db_isProfileValid, db_addProfile, db_getProfileInfo
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
        print(data)
        if not db_isProfileValid(data):
            r.set(db_getProfileInfo(data)) # На вход подаётся словарь с ID пользователя.

    return db_addProfile(data)


@auth_module.route('/', methods=['GET', 'POST'])
@auth_module.route('/login', methods=['GET', 'POST'])
def hLogin():
    r = initRedis_db()
    if request.method == 'POST':
        data = json.loads(request.data)

        if db_isProfileValid(data) and not r.get(db_getProfileInfo(data)):  # На вход подаётся словарь с данными пользователя. Возвращается его ID
            r.set(db_getProfileInfo(data), sha256(data['login'] + str(time.time())))
    return redirect('index')


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

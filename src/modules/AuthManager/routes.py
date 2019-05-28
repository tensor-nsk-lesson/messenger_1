from flask import Blueprint, request, redirect
from api.users import db_isProfileValid, db_addUser, db_getProfileInfo
from hashlib import sha256
from SessionControl.app import RedisSession
import time

auth_module = Blueprint('auth', __name__)


@auth_module.route('/register', methods=['GET', 'POST'])
def hRegister():
    r = RedisSession()
    if request.method == 'POST':
        data = request.from_json.to_dict()
        if not db_isProfileValid(data):
            db_addUser(data)
            r.set(db_getProfileInfo(data)) # На вход подаётся словарь с ID пользователя.

    return redirect('messages')


@auth_module.route('/login', methods=['GET', 'POST'])
def hLogin():
    r = RedisSession()
    if request.method == 'POST':
        data = request.from_json.to_dict()

        if db_isProfileValid(data) and not r.get(db_getProfileInfo(data)):  # На вход подаётся словарь с данными пользователя. Возвращается его ID
            r.set(db_getProfileInfo(data), sha256(data['login'] + str(time.time())))
    return redirect('index')


@auth_module.route('/logout')
def logout():
    data = request.from_json.to_dict() # Принимаем логин пользователя
    r = RedisSession()
    r.delete(db_getProfileInfo(data))
    return redirect('index')



@auth_module.route('/reset-password/', methods=['GET', 'POST'])
def hResetPW():
    r = RedisSession()

    if request.method == 'POST':
        data = request.from_json.to_dict()
        r.delete(db_getProfileInfo(data))
        #data.update({'password': sha256(data['password'].encode())})  # Хешируем введённый пользователем пароль
    return redirect('index')

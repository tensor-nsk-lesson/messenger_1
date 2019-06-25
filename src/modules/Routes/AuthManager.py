from flask import Blueprint, request, jsonify, abort
from modules.API.profile_methods import db_isAuthDataValid, db_addProfile, db_getUserIDbyEmail, db_getUserIDbyLogin
from modules.API.profile_methods import db_isProfileExists, db_updateProfileInfo, db_setActive
from modules.API.profile_methods import db_isEmailUsed
from modules.API.functions import isUserAuthorized, isUserDeleted, isUserBlocked
from modules.API.functions import sendConfirm, json_validate
from modules.API.functions import setSession, deleteSession, initRedis_db
from modules.json_schemas import login_schema, register_schema, password_schema
from hashlib import sha256
import jwt
import time
import re

auth_module = Blueprint('auth', __name__)


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

        if db_isEmailUsed(data):
            return jsonify({'status': 0, 'message': 'Такая почта уже зарегистрирована'})

        response = sendConfirm(data['email'], False)
        if type(response) == dict:
            return jsonify(response)

        return jsonify(db_addProfile(data))


@auth_module.route('/', methods=['POST'])
@auth_module.route('/login', methods=['POST'])
def hLogin():
    r = initRedis_db()
    if request.method == 'POST':
        if isUserAuthorized():
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

        if isUserBlocked(user_id):
            return jsonify({'status': 0, 'message': 'Данный аккаунт заблокирован'})
        elif isUserDeleted(user_id):
            return jsonify({'status': 0, 'message': 'Данный аккаунт удалён'})

        return setSession(user_id)


# TODO: Сделать валидацию JSON'а от пользователя
@auth_module.route('/logout', methods=['GET'])
def logout():
    if not isUserAuthorized():
        return jsonify({'status': 0, 'message': 'Вы не авторизованы'})

    UUID = request.cookies.get('SESSION')
    return deleteSession(UUID)


# TODO: Сделать валидацию JSON'а от пользователя

@auth_module.route('/reset-password')
def resetPW_request():
    email = request.args.get('email')
    if not email:
        return jsonify({'status': 0, 'message': 'Требуется параметр с email'})

    if ''.join(re.findall(r'^[0-9A-z-_]+@[0-9A-z-_]+.[0-9A-z]+$', email)) != email:
        return jsonify({'status': 0, 'message': 'Неправильный формат email\'а'})

    sendConfirm(email, True)
    return jsonify({'status': 1})



@auth_module.route('/reset-password/<token>', methods=['POST'])
def resetPW(token):
    r = initRedis_db()
    if request.method == 'POST':
        data = json_validate(request.data, password_schema)
        if not data:
            return abort(400)

        if not data['password']:
            return jsonify({'status': 0, 'message': 'Требуется пароль'})

        token_decoded = {}
        try:
            token_decoded.update(jwt.decode(token, 'uzE7lSw8Ch7X4aB81E22Z6Nh', algorithms=['HS256']))
        except Exception as err:
            print(err)

        if int(time.time() - token_decoded['time']) > 60*10:
            return jsonify({'status': 0, 'message': 'Токен просрочен'})

        user_id = db_getUserIDbyEmail(token_decoded)
        if not user_id:
            return jsonify({'status': 0, 'message': 'Пользователя с таким email не существует'})

        r.delete(user_id)
        return jsonify(db_updateProfileInfo(user_id, data, change_pw=True))


@auth_module.route('/confirm/<token>')
def confirmProfile(token):
    if request.method == 'GET':

        token_decoded = {}
        try:
            token_decoded.update(jwt.decode(token, 'uzE7lSw8Ch7X4aB81E22Z6Nh', algorithms=['HS256']))


            if int(time.time() - token_decoded['time']) > 60*10:
                return jsonify({'status': 0, 'message': 'Токен просрочен'})


            user_id = db_getUserIDbyEmail(token_decoded)
            if not user_id:
                return jsonify({'status': 0, 'message': 'Пользователя с таким email не существует'})

            db_setActive(user_id)
        except Exception as err:
            print(err)
            abort(400)

    return jsonify({'status': 1})

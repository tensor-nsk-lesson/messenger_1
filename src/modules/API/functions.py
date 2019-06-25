from modules.API.profile_methods import db_getProfileInfo
from modules.API.profile_methods import db_getUserIDbyEmail, db_setActive
from modules.API.profile_methods import db_setLastVisit
from messenger_1.src import app
from flask import url_for
from flask_mail import Mail, Message
from flask import request
from flask import make_response, redirect
from random import randint
import smtplib
import time
import jwt
import redis
import uuid
import json
import jsonschema


#####################
# SESSIONS
#####################

def initRedis_db():
    r = redis.Redis(host='localhost',port=6379, charset="utf-8", decode_responses=True)
    return r


def getUserID(uuid):
    r = initRedis_db()
    return r.get(uuid)


def setSession(user_id):
    r = initRedis_db()

    db_setLastVisit(user_id)

    salt = ''.join([chr(randint(97, 122)) for _ in range(32)])
    generate_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(user_id + time.time()) + salt))

    r.set(generate_uuid, user_id, ex=1000)
    response = make_response(redirect('/profile/{}'.format(user_id)))
    response.set_cookie('SESSION', bytes(generate_uuid, 'utf-8'))
    return response


def deleteSession(session):
    r = initRedis_db()
    r.delete(session)
    response = make_response(redirect('/profile/all'))
    response.delete_cookie('SESSION')
    return response



#####################
# PROFILE
#####################

def isUserBlocked(user_id):
    return db_getProfileInfo(user_id)['is_blocked']


def isUserDeleted(user_id):
    return db_getProfileInfo(user_id)['is_deleted']

def isUserAuthorized():
    return 'SESSION' in request.cookies.keys() and request.cookies['SESSION']



#####################
# MAIL
#####################

def sendConfirm(email, reset):
    mail = Mail(app)
    email_encoded = jwt.encode({'email': email, 'time': time.time()}, 'uzE7lSw8Ch7X4aB81E22Z6Nh', algorithm='HS256')
    msg = Message('Confirm Email', sender='mevomsngr@yandex.ru', recipients=[email])

    if reset:
        link = url_for('auth.resetPW', token=email_encoded, _external=True)
        msg.body = 'Здравствуйте! Был получен запрос на сброс пароля. Нажмите на ссылку для сброса пароля:\n{}\n\nЕсли вы не отправляли запрос на сброс пароля, то просто проигнорируйте это сообщение.'.format(link)
    else:
        link = url_for('auth.confirmProfile', token=email_encoded, _external=True)
        msg.body = 'Здравствуйте! В мессенджере MEVO был создан пользователь и привязан к Вашей почте. Чтобы подтвердить свой профиль, нажмите на ссылку:\n{}\n\nЕсли вы не регистрировались, то просто проигнорируйте это сообщение.'.format(link)
        user_id = db_getUserIDbyEmail(email)
        db_setActive(user_id)

    print(link)
    try:
        mail.send(msg)
    except smtplib.SMTPDataError:
        return {'status': 'Ошибка на сервере при попытке отправить сообщение'}



#####################
# JSON VALIDATOR
#####################

def json_validate(data_source, schema):
    try:
        data = json.loads(data_source)
        jsonschema.validate(data, schema)
        return data
    except (jsonschema.exceptions.ValidationError, json.decoder.JSONDecodeError) as err:
        print(err)
        data = None
        return data
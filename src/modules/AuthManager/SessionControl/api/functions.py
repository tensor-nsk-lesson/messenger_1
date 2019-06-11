from modules.ProfileManager.api.db_methods import db_setLastVisit
from flask import make_response, redirect
from random import randint
import time
import redis
import uuid


def initRedis_db():
    r = redis.Redis(host='localhost',port=6379)
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
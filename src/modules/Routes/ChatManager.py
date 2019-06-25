from flask import Blueprint, request, jsonify
from modules.API.chat_methods import db_addChat, db_addUserInChat, db_getMessagesFromChat
from modules.API.functions import json_validate, initRedis_db
from modules.json_schemas import chat_create_schema
from modules.API.functions import isUserAuthorized, isUserBlocked, isUserDeleted

messages_module = Blueprint('chats', __name__)

@messages_module.route('/<int:chatID>', methods=['GET, PUT, DELETE'])
def hChat(chatID):
    r = initRedis_db()
    if request.method == 'PUT':
        data = json_validate(request.data, chat_create_schema)

        if not isUserAuthorized():
            return jsonify({'status': 0, 'message': 'Требуется авторизация'})

        UUID = request.cookies.get('SESSION')
        user_id = r.get(UUID)

        if not data:
            return jsonify({'status': 0, 'message': 'Требуется запрос с JSON\'ом'})

        if not data['login'] or not data['content'] or not data['section_id']:
            return jsonify({'status': 0, 'message': 'Не заполнено имя конференции'})

        return jsonify(db_addUserInChat(user_id, chatID))


@messages_module.route('/create', methods=['PUT'])
def createChat():
    r = initRedis_db()
    if request.method == 'PUT':
        data = json_validate(request.data, chat_create_schema)

        if not isUserAuthorized():
            return jsonify({'status': 0, 'message': 'Требуется авторизация'})

        UUID = request.cookies.get('SESSION')
        user_id = int(r.get(UUID))

        if isUserBlocked(user_id):
            return jsonify({'status': 0, 'message': 'Аккаунт заблокирован'})

        if isUserDeleted(user_id):
            return jsonify({'status': 0, 'message': 'Аккаунт удалён'})

        if not data:
            return jsonify({'status': 0, 'message': 'Требуется запрос с JSON\'ом'})

        if not data['name']:
            return jsonify({'status': 0, 'message': 'Не заполнены данные о имени конференции'})

        print('---------- /create ---------')
        print(data, user_id)
        print(request.cookies.get('SESSION'))
        print('----------------------------')

        chatID = db_addChat(data)
        db_addUserInChat(user_id, chatID, permission=2)
        return jsonify({'status': 1, 'dialogID': chatID})


@messages_module.route('/get/all')
def getMessages(chat_id):
    if request.method == 'GET':
        return jsonify(db_getMessagesFromChat(chat_id))

@messages_module.route('/<int:chat_id>/useradd')
def addUserInChat(user_id):
    if request.method == 'POST':
        data = json_validate(request.data, chat_useradd_schema)

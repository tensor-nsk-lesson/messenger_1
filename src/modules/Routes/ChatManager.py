from flask import Blueprint, request, jsonify
from modules.API.chat_methods import db_addChat, db_addMessageForChat, db_addUserInChat, db_getMessagesFromChat
from modules.API.functions import json_validate
from modules.json_schemas import conference_create_schema
from modules.API.functions import initRedis_db

messages_module = Blueprint('messages', __name__)

@messages_module.route('/<int:chatID>', methods=['GET, PUT, DELETE'])
def send_message(chatID):
    r = initRedis_db()
    if request.method == 'PUT':
        data = json_validate(request.data, conference_create_schema)
        UUID = request.cookies.get('SESSION')
        user_id = r.get(UUID)

        if not data:
            return jsonify({'status': 0, 'message': 'Требуется запрос с JSON\'ом'})

        if not data['login'] or not data['content'] or not data['section_id']:
            return jsonify({'status': 0, 'message': 'Не заполнено имя конференции'})


        return jsonify(db_addMessageForChat(user_id, data['content'], chatID, 0))


@messages_module.route('/create', methods=['PUT'])
def create_chat():
    r = initRedis_db()
    if request.method == 'PUT':
        data = json_validate(request.data, conference_create_schema)
        print(data)
        print(request.cookies)
        if 'SESSION' not in request.cookies:
                return jsonify({'status': 0, 'message': 'Требуется авторизовация'})

        UUID = request.cookies.get('SESSION')
        user_id = r.get(UUID)
        if user_id is None:
            return jsonify({'status': 0, 'message': 'Требуется авторизация'})

        print(user_id)


        if not data:
            return jsonify({'status': 0, 'message': 'Требуется запрос с JSON\'ом'})

        if not data['name']:
            return jsonify({'status': 0, 'message': 'Не заполнены данные о имени конференции'})

        chatID = db_addChat(data)
        print(chatID)
        db_addUserInChat(user_id, chatID, permission=2)
        return jsonify({'status': 1, 'dialogID': chatID})


@messages_module.route('/get/<int:chat_id>')
def get_message(chat_id):
    if request.method == 'GET':
        return db_getMessagesFromChat(chat_id)


@messages_module.route('/get/all')
def get_messages(chat_id):
    if request.method == 'GET':
        return db_getMessagesFromChat(chat_id)
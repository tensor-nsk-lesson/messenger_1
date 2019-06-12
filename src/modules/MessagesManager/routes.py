from flask import Blueprint, request, jsonify
from modules.MessagesManager.api.functions import db_getMessage
from modules.MessagesManager.api.db_methods import db_addChat, db_addMessageForChat
from api.functions import getUserID
from modules.json_validator import json_validate
from modules.json_schemas import conference_create_schema


messages_module = Blueprint('messages', __name__)

@messages_module.route('/<int:chatID>', methods=['GET, PUT, DELETE'])
def send_message(chatID):
    if request.method == 'PUT':
        data = json_validate(request.data, conference_create_schema)
        UUID = request.cookies.get('SESSION')

        if not data:
            return jsonify({'status': 0, 'message': 'Требуется запрос с JSON\'ом'})

        if not data['login'] or not data['content'] or not data['section_id']:
            return jsonify({'status': 0, 'message': 'Не заполнено имя конференции'})

        user_id = getUserID(UUID)
        return jsonify(db_addMessageForChat(user_id, data['content'], chatID, 0))


@messages_module.route('/create', methods=['PUT'])
def create_chat():
    if request.method == 'PUT':
        data = json_validate(request.data, conference_create_schema)

        if not data:
            return jsonify({'status': 0, 'message': 'Требуется запрос с JSON\'ом'})

        if not data['name']:
            return jsonify({'status': 0, 'message': 'Не заполнены данные о имени конференции'})
        chatID = db_addChat(data)
        return jsonify({'status': 1, 'dialogID': chatID})


@messages_module.route('/get/<int:chat_id>')
def get_message(chat_id):
    if request.method == 'GET':
        return db_getMessage(chat_id)


@messages_module.route('/all')
def get_messages(chat_id):
    if request.method == 'GET':
        return db_getMessage(chat_id)
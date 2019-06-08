from flask import Blueprint, request, jsonify
from modules.MessagesManager.api.functions import db_getMessage, db_sendMessage
from modules.MessagesManager.api.db_methods import db_addDialog, db_addMessageForDialog, db_addUserInDialog
from modules.MessagesManager.api.db_methods import db_getMessagesFromDialog
from modules.AuthManager.SessionControl.app import getUserID
from modules.json_validator import json_validate
from modules.json_schemas import conference_create_schema


messages_module = Blueprint('messages', __name__)

@messages_module.route('/<int:dialogID>', methods=['GET, PUT, DELETE'])
def send_message(dialogID):
    if request.method == 'PUT':
        data = json_validate(request.data, conference_create_schema)
        UUID = request.cookies.get('SESSION')

        if not data:
            return jsonify({'status': 0, 'message': 'Требуется запрос с JSON\'ом'})

        if not data['login'] or not data['content'] or not data['section_id']:
            return jsonify({'status': 0, 'message': 'Не заполнены данные о имени конференции'})

        user_id = getUserID(UUID)
        return jsonify(db_addMessageForDialog(user_id, data['content'], dialogID, 0))


@messages_module.route('/create', methods=['PUT'])
def create_chat():
    if request.method == 'PUT':
        data = json_validate(request.data, conference_create_schema)

        if not data:
            return jsonify({'status': 0, 'message': 'Требуется запрос с JSON\'ом'})

        if not data['name']:
            return jsonify({'status': 0, 'message': 'Не заполнены данные о имени конференции'})
        dialogID = db_addDialog(data)
        return jsonify({'status': 1, 'dialogID': dialogID})


@messages_module.route('/get/<int:dialog_id>')
def get_message(dialog_id):
    if request.method == 'GET':
        return db_getMessage(dialog_id)


@messages_module.route('/all')
def get_messages(dialog_id):
    if request.method == 'GET':
        return db_getMessage(dialog_id)
from flask import Blueprint, request, jsonify
from db_handle import db_getProfileInfo, db_updateProfileInfo, db_getProfilesInfo, db_addUser, db_sendMessage, db_getMessage, db_delUser

api_module = Blueprint('api', __name__)


@api_module.route('/profile/<int:ID>', methods=['GET', 'PUT', 'DELETE'])
def profile(ID):
    if request.method == 'GET':
        return jsonify(db_getProfileInfo(ID))

    elif request.method == 'PUT':
        db_updateProfileInfo(ID, request.json.to_dict)
        return jsonify({'message': 'User data has been updated'})

    elif request.method == 'DELETE':
        db_delUser(ID, request.json.to_dict)


@api_module.route('/profiles')
def profiles():
    return jsonify(db_getProfilesInfo())


@api_module.route('/profile/create')
def create_profile():
    if request.method == 'POST':
        db_addUser(request.get_json())
        return jsonify({'status': 1})


@api_module.route('/message/send/')
def send_message():
    if request.method == 'PUT':
        db_sendMessage(request.get_json())
        return jsonify({'status': 1})


@api_module.route('/messages/<int:dialog_id>')
def get_message(dialog_id):
    if request.method == 'GET':
        return jsonify(db_getMessage(dialog_id))



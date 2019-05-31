from flask import Blueprint, request, jsonify
from modules.db_methods import db_delProfile, db_getProfileInfo, db_getProfilesInfo, db_updateProfileInfo

from modules.ProfileManager.api.functions import isProfileDeleted, isProfileBlocked
import json

profile_module = Blueprint('profile', __name__)

@profile_module.route('/profile/<int:ID>', methods=['GET', 'PUT', 'DELETE'])
def profile(ID):
    if request.method == 'GET':
        return jsonify(db_getProfileInfo(ID))

    else:
        data = json.loads(request.data)
        if request.method == 'PUT':
            if isProfileDeleted(ID):
                return jsonify({'status': 0, 'message': 'Невозможно изменить данные удалённого аккаунта'})

            if isProfileBlocked(ID):
                return jsonify({'status': 0, 'message': 'Невозможно изменить данные заблокированного'})

            return jsonify(db_updateProfileInfo(ID, data))

        elif request.method == 'DELETE':
            if isProfileDeleted(ID):
                return jsonify({'status': 0, 'message': 'Аккаунт уже удалён'})

            return db_delProfile(ID)


@profile_module.route('/profiles')
def profiles():
    return jsonify(db_getProfilesInfo())
from flask import Blueprint, request, jsonify, abort
from modules.ProfileManager.api.db_methods import db_delProfile, db_getProfileInfo, db_getProfilesInfo, db_updateProfileInfo
from modules.ProfileManager.api.db_methods import db_FullDelProfile, db_isProfileExists
from modules.ProfileManager.api.functions import isProfileDeleted, isProfileBlocked
from modules.json_validator import json_validate
from modules.json_schemas import profile_update_schema
import json

profile_module = Blueprint('profile', __name__)

@profile_module.route('/<int:ID>', methods=['GET', 'PUT', 'DELETE'])
def profile(ID):
    if not db_isProfileExists(ID):
        return jsonify({'status': 0, 'message': 'Такого аккаунта не существует'})

    if request.method == 'GET':
        return jsonify(db_getProfileInfo(ID))

    else:
        if request.method == 'PUT':

            data = json_validate(request.data, profile_update_schema)

            if data is None:
                abort(400)

            if isProfileDeleted(ID):
                return jsonify({'status': 0, 'message': 'Невозможно изменить данные удалённого аккаунта'})

            if isProfileBlocked(ID):
                return jsonify({'status': 0, 'message': 'Невозможно изменить данные заблокированного аккаунта'})

            return jsonify(db_updateProfileInfo(ID, data))

        elif request.method == 'DELETE':
            if isProfileDeleted(ID):
                return jsonify({'status': 0, 'message': 'Аккаунт уже удалён'})

            #return db_delProfile(ID, status=True)
            return jsonify(db_FullDelProfile(ID))


@profile_module.route('/all')
def profiles():
    return jsonify(db_getProfilesInfo())

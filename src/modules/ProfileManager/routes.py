from flask import Blueprint, request, redirect, jsonify
from api.users import db_addProfile, db_delProfile, db_getProfileInfo, db_getProfilesInfo, db_updateProfileInfo, db_isProfileValid
import json

profile_module = Blueprint('profile', __name__)

@profile_module.route('/profile/<int:ID>', methods=['GET', 'PUT', 'DELETE'])
def profile(ID):
    if request.method == 'GET':
        return jsonify(db_getProfileInfo(ID))

    else:
        data = json.loads(request.data)
        if request.method == 'PUT':
            return jsonify(db_updateProfileInfo(ID, data))

        elif request.method == 'DELETE':
            return db_delProfile(ID)


@profile_module.route('/profiles')
def profiles():
    return jsonify(db_getProfilesInfo())
from flask import Blueprint, request
from api.users import db_addUser, db_delProfile, db_getProfileInfo, db_getProfilesInfo, db_updateProfileInfo, db_isProfileValid

profile_module = Blueprint('profile', __name__)

@profile_module.route('/profile/<int:ID>', methods=['GET', 'PUT', 'DELETE'])
def profile(ID):
    if request.method == 'GET':
        return db_getProfileInfo(ID)

    elif request.method == 'PUT':
        return db_updateProfileInfo(ID, request.json.to_dict)

    elif request.method == 'DELETE':
        return db_delProfile(ID, request.json.to_dict)


@profile_module.route('/profiles')
def profiles():
    return db_getProfilesInfo()


@profile_module.route('/profile/create')
def create_profile():
    if request.method == 'POST':
        data = request.from_json.to_dict()
        if not db_isProfileValid(data):
            return db_addUser(request.get_json())




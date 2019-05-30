from flask import Blueprint, request, redirect
from api.users import db_addProfile, db_delProfile, db_getProfileInfo, db_getProfilesInfo, db_updateProfileInfo, db_isProfileValid
import json

profile_module = Blueprint('profile', __name__)

@profile_module.route('/profile/<int:ID>', methods=['GET', 'PUT', 'DELETE'])
def profile(ID):
    data = json.loads(request.data)
    if request.method == 'GET':
        return db_getProfileInfo(ID)

    elif request.method == 'PUT':
        return db_updateProfileInfo(ID, data)

    elif request.method == 'DELETE':
        return db_delProfile(ID, data)


@profile_module.route('/profiles')
def profiles():
    return db_getProfilesInfo()


@profile_module.route('/profile/create', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        data = json.loads(request.data)
        print(data)
        if not db_isProfileValid(data):
            db_addProfile(data)

    return redirect('profiles')
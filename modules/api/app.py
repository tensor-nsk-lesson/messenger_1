from flask import Blueprint, request, jsonify
from db_handle import db_getProfileInfo, db_updateProfileInfo, db_delUser, db_getProfilesInfo

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/profile/<int:ID>', methods=['GET', 'PUT', 'DELETE'])
def profile(ID):
    if request.method == 'GET':
        return jsonify(db_getProfileInfo(ID))

    elif request.method == 'PUT':
        db_updateProfileInfo(ID, request.json.to_dict)

    elif request.method == 'DELETE':
        db_delUser(ID, request.json.to_dict)


@api_blueprint.route('/profiles')
def profiles():
    return jsonify(db_getProfilesInfo())

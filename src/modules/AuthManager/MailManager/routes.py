from flask import Blueprint, jsonify

from itsdangerous import URLSafeTimedSerializer
from modules.AuthManager.MailManager.api.functions import isTokenExpired


mail_module = Blueprint('mailManager', __name__)

s = URLSafeTimedSerializer('uzE7lSw8Ch7X4aB81E22Z6Nh')

@mail_module.route('/confirm/<token>', methods=['GET', 'PUT'])
def confirm_email(token):
    if isTokenExpired(token):
        return jsonify({'status': 0, 'message': 'Токен просрочился'})

    #db_setProfileActivate()
    return {'status': 1}
from src.app import app
from flask import url_for
from flask_mail import Mail, Message
from modules.ProfileManager.api.db_methods import db_getUserIDbyEmail, db_setActive
import time
import jwt


def sendConfirm(email, reset=False):
    mail = Mail(app)
    email_encoded = jwt.encode({'email': email, 'time': time.time()}, 'uzE7lSw8Ch7X4aB81E22Z6Nh', algorithm='HS256')
    msg = Message('Confirm Email', sender='mevomsngr@yandex.ru', recipients=[email])

    if reset:
        link = url_for('auth.resetPW', token=email_encoded, _external=True)
        msg.body = 'Ссылка для сброса пароля: {}. Если вы не отправляли запрос на сброс пароля, то просто проигнорируйте это сообщение.'.format(link)
    else:
        link = url_for('auth.confirmProfile', token=email_encoded, _external=True)
        msg.body = 'Был создан пользователь в мессенджере MEVO. Чтобы подтвердить свой профиль, нажмите на ссылку. Если вы не отправляли запрос на сброс пароля, то просто проигнорируйте это сообщение.'.format(link)
        user_id = db_getUserIDbyEmail(email)
        db_setActive(user_id)

    print(link)
    mail.send(msg)

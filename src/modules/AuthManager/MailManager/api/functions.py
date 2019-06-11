from flask import url_for
from flask_mail import Mail, Message
from modules.AuthManager.routes import resetPW
from src.app import app
from itsdangerous import SignatureExpired, URLSafeTimedSerializer

s = URLSafeTimedSerializer('uzE7lSw8Ch7X4aB81E22Z6Nh')

def send_message_confirm_reset_pw(email):
    mail = Mail(app)
    token = s.dumps(email, salt=app.config['SECRET_KEY'])
    msg = Message('Confirm Email', sender='mevomsngr@yandex.ru', recipients=[email])
    link = url_for('resetPW', token=token, _external=True)
    msg.body = 'Ссылка для сброса пароля: {}. Если вы не отправляли запрос на сброс пароля, то просто проигнорируйте это сообщение.'.format(link)
    mail.send(msg)


def isTokenExpired(token):
    try:
        s.loads(token, salt=app.config['SECRET_KEY'], max_age=60)
    except SignatureExpired:
        return True
    return False
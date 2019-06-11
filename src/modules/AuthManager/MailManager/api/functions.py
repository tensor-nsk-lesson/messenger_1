from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from src.app import app




def isTokenExpired(token):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    try:
        s.loads(token, salt=app.config['SECRET_KEY'], max_age=60)
    except SignatureExpired:
        return True
    return False
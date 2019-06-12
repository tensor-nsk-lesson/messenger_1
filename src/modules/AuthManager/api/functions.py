from flask import request

def isUserAuthorized():
    return 'SESSION' in request.cookies.keys() and request.cookies['SESSION']
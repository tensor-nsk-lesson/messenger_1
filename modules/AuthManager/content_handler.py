import re

def FormContainHandler(text):
    return re.sub(r'(\'[a-zA-Z]\')', text)
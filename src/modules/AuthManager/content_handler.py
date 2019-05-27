# -*- coding: utf-8 -*
import re

def FormContainHandler(dict):
    print(dict)
    for key in dict:
        value = u'dict[key]'
        if key != 'login':
            dict.update({key: re.sub(r'[^a-zA-Z]', '', value)})
        else:
            dict.update({key: re.sub(r'[^\W]', '', value)})
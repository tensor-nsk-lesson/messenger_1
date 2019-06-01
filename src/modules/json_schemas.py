login_schema = {
    'type': 'object',
    'properties': {
        'login': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['login', 'password']
}


register_schema = {
    'type': 'object',
    'properties': {
        'login': {'type': 'string'},
        'password': {'type': 'string'},
        'first_name': {'type': 'string'},
        'second_name': {'type': 'string'}
    },
    'required': ['login', 'password', 'first_name', 'second_name']
}

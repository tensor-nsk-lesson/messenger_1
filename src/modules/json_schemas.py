login_schema = {
    'type': 'object',
    'properties': {
        'login': {'type': 'string', 'pattern': '^[0-9A-z-_]+$'},
        'password': {'type': 'string', 'pattern': '^[0-9A-z-_]+$'}
    },
    'required': ['login', 'password']
}


register_schema = {
    'type': 'object',
    'properties': {
        'login': {'type': 'string', 'pattern': '^[0-9A-z-_]+$'},
        'email': {'type': 'string', 'pattern': '^[0-9A-z-_]+@[0-9A-z-_]+.[0-9A-z]+$'},
        'password': {'type': 'string', 'pattern': '^[0-9A-z-_]+$'},
        'first_name': {'type': 'string', 'pattern': '^[0-9A-z-_]+$'},
        'second_name': {'type': 'string', 'pattern': '^[0-9A-z-_]+$'}
    },
    'required': ['login', 'password', 'first_name', 'second_name']
}


profile_update_schema = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string', 'pattern': '^[0-9A-z-_]+$'},
        'second_name': {'type': 'string', 'pattern': '^[0-9A-z-_]+$'}
    },
    'required': ['first_name', 'second_name']
}


conference_create_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', 'pattern': '^[0-9A-z-_]+$'},
    },
    'required': ['name']
}

conference_send_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', 'pattern': '^[0-9A-z-_]+$'},
    },
    'required': ['name']
}

email_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string', 'pattern': '^[0-9A-z-_]+@[0-9A-z-_]+.[0-9A-z]+$'},
    },
    'required': ['email']
}
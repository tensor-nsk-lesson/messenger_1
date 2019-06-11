login_schema = {
    'type': 'object',
    'properties': {
        'login': {'type': 'string', 'pattern': '^\w+$'},
        'password': {'type': 'string', 'pattern': '^\w+$'}
    },
    'required': ['login', 'password']
}


register_schema = {
    'type': 'object',
    'properties': {
        'login': {'type': 'string', 'pattern': '^\w+$'},
        'password': {'type': 'string', 'pattern': '^\w+$'},
        'first_name': {'type': 'string', 'pattern': '^\w+$'},
        'second_name': {'type': 'string', 'pattern': '^\w+$'},
        'email': {'type': 'string', 'pattern': '^\w+$'}
    },
    'required': ['login', 'password', 'first_name', 'second_name', 'email']
}


profile_update_schema = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string', 'pattern': '^\w+$'},
        'second_name': {'type': 'string', 'pattern': '^\w+$'}
    },
    'required': ['first_name', 'second_name']
}


conference_create_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', 'pattern': '^\w+$'},
    },
    'required': ['name']
}

conference_send_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', 'pattern': '^\w+$'},
    },
    'required': ['name']
}
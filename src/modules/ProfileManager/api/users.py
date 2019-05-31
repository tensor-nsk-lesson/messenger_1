from database import sql_execute
from flask import jsonify

def db_addProfile(data):
    if not db_isProfileExists(data):
        sql="""
            INSERT INTO users (first_name, second_name, created_at, last_visit, is_blocked, is_active, is_deleted) 
            VALUES ('{first_name}', '{second_name}', NOW(), NOW(), false, true, false) RETURNING id;
        """.format(**data)
        user_id = sql_execute(sql, True)
        sql = """
            INSERT INTO authentications (user_id, login, password) 
            VALUES ('{}', '{login}', '{password}');
        """.format(user_id[0]['id'], **data)
        sql_execute(sql, fetch_all=False)
        return {'status': 1}
    else:
        return {'status': 0, 'message': 'Такой логин уже зарегистрирован.'}


def db_delProfile(ID):
    # TODO: Добавить запрос на удаление пользователя
    sql='''
        UPDATE users 
        SET is_deleted = true
        WHERE id='{ID}';
    '''.format(ID)
    return sql_execute(sql, fetch_all=True)


def db_isProfileValid(data):
    sql='''
        SELECT user_id
        FROM authentications
        WHERE (login='{login}' AND password='{password}');
    '''.format(**data)
    answer = sql_execute(sql, fetch_all=False)
    return bool(answer['user_id'])


def db_isProfileExists(data):
    sql='''
        SELECT count(user_id)
        FROM authentications
        where login='{login}';
    '''.format(**data)
    users = sql_execute(sql, fetch_all=False)['count']
    return bool(users)


def db_setLastVisit(ID):
    sql='''
        UPDATE users
        SET last_visit = NOW()
        where id='{}'
    '''.format(ID)
    sql_execute(sql, fetch_all=False)


# TODO: Сделать ещё возвращение ID.
def db_getProfileInfo(ID):
    sql='''
        SELECT first_name, second_name, created_at, last_visit 
        FROM users
        WHERE id='{}';
    '''.format(ID)
    return sql_execute(sql, fetch_all=False)


def db_getUserID(data):
    sql='''
        SELECT user_id
        FROM authentications
        where login='{login}';
    '''.format(**data)
    user_id = sql_execute(sql, fetch_all=False)
    return user_id['user_id']


def db_updateProfileInfo(ID, data):
    sql = ''
    for key in data, ('first_name', 'second_name'):
        if data[key]:
            sql='''
                UPDATE users
                SET {1}='{2}' 
                WHERE id='{3}';
            '''.format(key, data[key], ID)
    return sql_execute(sql, fetch_all=False)


def db_getProfilesInfo():
    sql='''
        SELECT first_name, second_name, id, last_visit, is_deleted 
        FROM Users;
    '''
    return sql_execute(sql, fetch_all=True)




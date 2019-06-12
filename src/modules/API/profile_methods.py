from modules.API.sql_execute import sql_execute
from hashlib import sha256

## DEVELOP METHODS
def db_addProfile(data):
    data.update({'password': sha256(data['password'].encode()).hexdigest()})
    sql='''
        INSERT INTO users (first_name, second_name, created_at, last_visit, is_blocked, is_online, is_deleted, is_confirmed) 
        VALUES ('{first_name}', '{second_name}', NOW(), NOW(), false, false, false, false) 
        RETURNING id;
    '''.format(**data)
    user_id = sql_execute(sql, fetch_all=True)
    sql = """
        INSERT INTO auth (user_id, login, password, email) 
        VALUES ('{:d}', '{login}', '{password}', '{email}');
    """.format(user_id[0]['id'], **data)
    sql_execute(sql, fetch_all=False)
    return {'status': 1, 'message': 'На Вашу почту было отправлено сообщение ссылкой подтверждения. Перейдите по ней.'}


def db_isAuthDataValid(data):
    print('-- db_isAuthDataValid() --')
    print(data)
    sql='''
        SELECT user_id
        FROM auth
        WHERE login='{login}' AND password='{password}';
    '''.format(**data)
    answer = sql_execute(sql, fetch_all=False)
    print(answer)
    print('------------------------')

    if not answer:
        return False
    else:
        return True


def db_isProfileExists(data):
    sql = "SELECT count(login) FROM auth"

    if type(data) == int:
        sql += " WHERE user_id='{:d}';".format(data)
    elif type(data) == dict:
        sql += " WHERE login='{login}';".format(**data)


    users = sql_execute(sql, fetch_all=False)['count']
    return bool(users)


def db_setLastVisit(ID):
    sql='''
        UPDATE users
        SET last_visit = NOW()
        WHERE id='{:d}';
    '''.format(ID)
    sql_execute(sql, fetch_all=False)


def db_setActive(ID, status=True):
    sql='''
        UPDATE users
        SET is_confirmed='{}'
        WHERE id='{:d}'
    '''.format(status, ID)
    sql_execute(sql, fetch_all=False)


def db_setOnline(ID, status=True):
    sql='''
        UPDATE users
        SET is_online='{}'
        WHERE id='{:d}'
    '''.format(status, ID)
    sql_execute(sql, fetch_all=False)


""" 
# Функция блокирует пользователя. 
По дефолту стоит True, поэтому аргумент status можно не отправлять. 
Если передать False, то разблокирует.
"""
def db_blockProfile(ID, status=True):
    sql='''
        UPDATE users
        SET is_blocked='{}'
        WHERE id='{:d}';
    '''.format(status, ID)
    sql_execute(sql, fetch_all=False)


def db_getUserIDbyLogin(data):
    sql="SELECT user_id FROM auth WHERE login='{login}';".format(**data)
    user_id = sql_execute(sql, fetch_all=False)
    return False if user_id is None else user_id['user_id']


def db_getUserIDbyEmail(data):
    if type(data) == str:
        sql="SELECT user_id FROM auth WHERE email='{}'".format(data)
    elif type(data) == dict:
        sql = "SELECT user_id FROM auth WHERE email='{email}'".format(**data)
    user_id = sql_execute(sql, fetch_all=False)
    return False if user_id is None else user_id['user_id']


## PUBLIC METHODS
""" 
# Функция удаляет профиль пользователя. 
По дефолту стоит True, поэтому аргумент status можно не отправлять. 
Если передать False, то восстанавливает.
"""
def db_delProfile(ID, status=True):
    # TODO: Добавить запрос на удаление пользователя
    sql='''
        UPDATE users
        SET is_deleted='{}'
        WHERE id='{:d}';
    '''.format(status, ID)
    return sql_execute(sql, fetch_all=True)


def db_FullDelProfile(ID):
    # TODO: Добавить запрос на удаление пользователя
    sql='''
        DELETE FROM auth
        WHERE user_id='{:d}';
        DELETE FROM users
        WHERE id='{:d}';
    '''.format(ID, ID)
    sql_execute(sql, fetch_all=True)
    return {'status': 1}


def db_getProfileInfo(ID):
    sql='''
        SELECT *
        FROM users
        WHERE id='{:d}';
    '''.format(ID)
    return sql_execute(sql, fetch_all=False)


def db_getProfilesInfo():
    sql='''
        SELECT *
        FROM users;
    '''
    return sql_execute(sql, fetch_all=True)


def db_updateProfileInfo(ID, data, change_pw=False):
    rows = []
    if 'password' in data.keys():
        data.update({'password': sha256(data['password'].encode()).hexdigest()})

    for key in data:
        if not change_pw:
            if not key in ('first_name', 'second_name'):
                return {'status': 0, 'message': 'Неизвестное поле. Менять можно только first_name/second_name'}
        else:
            if not key in 'password':
                return {'status': 0, 'message': 'Неизвестное поле. Менять можно только password'}

            if data[key]:
                if not change_pw:
                    sql='''
                        SELECT first_name, second_name
                        FROM users
                        WHERE id='{:d}'
                    '''.format(ID)
                else:
                    sql = '''
                        SELECT password
                        FROM auth
                        WHERE user_id='{:d}'
                    '''.format(ID)
                answer = sql_execute(sql, fetch_all=False)

                if data[key] == answer[key]: # Если введённое и из БД поля эквиваленты, то выкидываем ошибку.
                    rows.append(key)
                    continue

                if not change_pw:
                    sql = '''
                        UPDATE users
                        SET {}='{}' 
                        WHERE id='{:d}';
                    '''.format(key, data[key], ID)
                else:
                    sql = '''
                        UPDATE auth
                        SET password='{}'
                        WHERE user_id='{:d}'
                    '''.format(data['password'], ID)

                sql_execute(sql, fetch_all=False)

    if not len(rows):
        return {'status': 1}
    elif len(rows) >= 1:
        return {'status': 1, 'message': 'Эквивалентное поле {} не было изменено'.format(rows)}
    else:
        return {'status': 0, 'message': 'Эквивалентные поля {} не были изменены'.format(rows)}
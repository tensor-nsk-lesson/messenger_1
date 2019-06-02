from modules.database import sql_execute


## DEVELOP METHODS
def db_addProfile(data):
    sql = ("INSERT INTO users (first_name, second_name, created_at, last_visit, is_blocked, is_online, is_deleted)\n"
           "VALUES ('%(first_name)s', '%(second_name)s', NOW(), NOW(), false, true, false)\n"
           "RETURNING id;"
           ) % data
    user_id = sql_execute(sql, False)
    sql = ("INSERT INTO authentications (user_id, login, password)\n"
           "VALUES (%d, '%(login)s', '%(password)s');"
           ) % user_id[0]['id'], data
    sql_execute(sql, False)
    return {'status': 1}


def db_isAuthDataValid(data):
    sql = ("SELECT user_id\n"
           "FROM authentications\n"
           "WHERE login='%(login)s' AND password='%(password)s';"
           ) % data
    answer = sql_execute(sql, False)
    return bool(answer['user_id'])


def db_isProfileExists(data):
    sql = ("SELECT count(login)\n"
           "FROM authentications")
    if type(data) == int:
        sql += "WHERE user_id='%d'" % data
    elif type(data) == dict:
        sql += "WHERE login='$(login)s';" % data

    users = sql_execute(sql, False)['count']
    return bool(users)


def db_setLastVisit(ID):
    sql = ("UPDATE users\n"
           "SET last_visit = NOW()\n"
           "WHERE id='%d';"
           ) % ID
    sql_execute(sql, False)


""" 
# Функция блокирует пользователя. 
По дефолту стоит True, поэтому аргумент status можно не отправлять. 
Если передать False, то разблокирует.
"""


def db_blockProfile(ID, status=True):
    sql = ("UPDATE users\n"
           "SET is_blocked='%s'\n"
           "WHERE id='%d';"
           ) % (status, ID)
    sql_execute(sql, False)


def db_getUserID(data):
    sql = ("SELECT user_id\n"
           "FROM authentications\n"
           "WHERE login='%(login)s';"
           ) % data
    user_id = sql_execute(sql, False)
    return user_id['user_id']


## PUBLIC METHODS
""" 
# Функция удаляет профиль пользователя. 
По дефолту стоит True, поэтому аргумент status можно не отправлять. 
Если передать False, то восстанавливает.
"""


def db_delProfile(ID, status=True):
    sql = ("UPDATE users\n"
           "SET is_deleted=%s\n"
           "WHERE id=%d"
           ) % (status, ID)
    return sql_execute(sql)
    ''' % (status, ID)
    sql_execute(sql, fetch_all=True)
    return {'status': 1}


def db_FullDelProfile(ID):
    # TODO: Добавить запрос на удаление пользователя
    sql = ("DELETE FROM authentications\n"
           "WHERE user_id='%d';\n"
           "DELETE FROM users\n"
           "WHERE id=\'%d\';"
           ) % (ID, ID)
    sql_execute(sql, True)
    return {'status': 1}


def db_getProfileInfo(ID):
    sql = ("SELECT first_name, second_name, id, last_visit, is_deleted, is_blocked\n"
           "FROM users\n"
           "WHERE id='%d';"
           ) % ID
    return sql_execute(sql, False)


def db_getProfilesInfo():
    sql = ("SELECT first_name, second_name, id, last_visit, is_deleted, is_blocked, is_online\n"
           "FROM users;"
           )
    return sql_execute(sql)


def db_updateProfileInfo(ID, data):
    rows = []
    for key in data:
        if not key in ('first_name', 'second_name'):
            return {'status': 0, 'message': 'Неизвестное поле. Менять можно только first_name/second_name'}

        if data[key]:
            sql = ("SELECT first_name, second_name\n"
                   "FROM users\n"
                   "WHERE id='%d';"
                   ) % ID
            answer = sql_execute(sql, False)

            if data[key] == answer[key]:  # Если введённое и из БД поля эквиваленты, то выкидываем ошибку.
                rows.append(key)
                continue

            sql = ("UPDATE users\n"
                   "SET %s='%s' \n"
                   "WHERE id='%d';"
                   ) % (key, data[key], ID)
            sql_execute(sql, False)

    if not len(rows):
        return {'status': 1}
    elif len(rows) >= 1:
        return {'status': 1, 'message': 'Эквивалентное поле {} не было изменено'.format(rows)}
    else:
        return {'status': 0, 'message': 'Эквивалентные поля {} не были изменены'.format(rows)}

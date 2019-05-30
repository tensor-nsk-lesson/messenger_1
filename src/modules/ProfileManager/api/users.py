from database import sql_execute

def db_addProfile(data):
    sql="""
        INSERT INTO users (first_name, second_name, created_at, last_visit, is_blocked, is_active, is_deleted) 
        VALUES ('{first_name}', '{second_name}', NOW(), NOW(), false, true, false) RETURNING id;
    """.format(**data)
    userid = sql_execute(sql, True)
    print(sql)
    sql = """
        INSERT INTO authentications (user_id, login, password) 
        VALUES ('{}', '{login}', '{password}');
    """.format(userid[0]['id'], **data)
    print(sql)
    sql_execute(sql, True)


def db_delProfile(ID):
    # TODO: Добавить запрос на удаление пользователя
    sql="""
        UPDATE users 
        SET is_deleted = true
        WHERE id='{ID}';
    """.format(ID)
    return sql_execute(sql, True)


def db_isUserCreated(data):
    sql="""
        SELECT count(id) 
        FROM authentications 
        WHERE login='{login}'};
    """.format(**data)
    return sql_execute(sql, False) == 1


# TODO: Сделать ещё возвращение ID.
def db_getProfileInfo(ID):
    sql="""
        SELECT first_name, last_name, created_at, last_visit 
        FROM User
        WHERE id='{ID}';
    """.format(ID)
    return sql_execute(sql, False)


def db_updateProfileInfo(ID, data):
    for key in data:
        if data[key]:
            sql="""
                UPDATE User
                SET {1}='{2}' 
                WHERE id='{3}';
            """.format(key, data[key], ID)
    return sql_execute(sql, False)


def db_getProfilesInfo():
    sql="""
        SELECT * 
        FROM Users;
    """
    return sql_execute(sql, False)


def db_isProfileValid(data):
    sql="""
        SELECT count(user_id)
        FROM authentications
        WHERE login='{login}' 
        AND password='{password}';
    """.format(**data)
    return sql_execute(sql, False)

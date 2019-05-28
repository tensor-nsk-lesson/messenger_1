from database import sql_execute

def db_addUser(data):
    sql="""
        INSERT INTO User (first_name, last_name) 
        VALUES ({firstname},{secondname});
        INSERT INTO Authentication (login, password) 
        VALUES ({login},{password});
    """.format(**data)
    sql_execute(sql, True)


def db_delProfile(ID, token):
    # TODO: Добавить запрос на удаление пользователя
    sql="""
        UPDATE users 
        SET is_deleted = true 
        WHERE id = {ID} and token;
    """.format(ID, token)
    return sql_execute(sql, True)


def db_isUserCreated(data):
    sql="""
        SELECT count(id) 
        FROM Authentication 
        WHERE login={login}};
    """.format(**data)
    return sql_execute(sql, False) == 1


# TODO: Сделать ещё возвращение ID.
def db_getProfileInfo(ID):
    sql="""
        SELECT first_name, last_name, created_at, last_visit 
        FROM User
        WHERE id={ID};
    """.format(ID)
    return sql_execute(sql, False)


def db_updateProfileInfo(ID, data):
    for key in data:
        if data[key]:
            sql="""
                UPDATE User
                SET {1}={2} 
                WHERE id={3};
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
        SELECT count(password) 
        FROM Authenticaton
        WHERE login={login} 
        AND password={password};
    """.format(**data)
    return sql_execute(sql, False)['status'] == 1

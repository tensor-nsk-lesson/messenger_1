from modules.database import sql_execute

def db_addProfile(data):
    sql= ("INSERT INTO users (first_name, second_name, created_at, last_visit, is_blocked, is_active, is_deleted)\n"
          "VALUES ('{first_name}', '{second_name}', NOW(), NOW(), false, true, false)\n"
          "RETURNING id"
          ).format(**data)
    userid = sql_execute(sql)
    print(sql)
    sql = ("INSERT INTO authentications (user_id, login, password) \n"
           "VALUES ({}, '{login}', '{password}')"
           ).format(userid[0]['id'], **data)
    print(sql)
    sql_execute(sql)

def db_delProfile(ID):
    sql= ("UPDATE users\n"
          "SET is_deleted = true\n"
          "WHERE id = {ID}"
          ).format(ID)
    return sql_execute(sql)

def db_isUserCreated(data):
    sql= ("SELECT count(user_id)\n"
          "FROM authentications\n"
          "WHERE login = '{login}'"
          ).format(**data)
    return True if sql_execute(sql, False) else False

def db_getProfileInfo(ID):
    sql= ("SELECT id, first_name, second_name, created_at, last_visit\n"
          "FROM users\n"
          "WHERE id = {ID}"
          ).format(ID)
    return sql_execute(sql, False)

def db_getUserID(data):
    sql= ("SELECT user_id\n"
          "FROM authentications\n"
          "where login='{login}'"
          ).format(**data)
    user_id = sql_execute(sql, False)
    return user_id['user_id']

def db_updateProfileInfo(ID, data):
    for key in data:
        if data[key]:
            sql= ("UPDATE users\n"
                  "SET {1} = '{2}'\n"
                  "WHERE id = {3}"
                  ).format(key, data[key], ID)
    return sql_execute(sql, False)

def db_getProfilesInfo():
    sql= ("SELECT * FROM users")
    return sql_execute(sql, False)

def db_isProfileValid(data):
    sql= ("SELECT count(user_id)\n"
          "FROM authentications\n"
          "WHERE login='{login}'\n"
          "AND password='{password}'"
          ).format(**data)
    return True if sql_execute(sql, False) else False

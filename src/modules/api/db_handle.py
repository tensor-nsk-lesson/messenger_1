import psycopg2
from psycopg2.extras import RealDictCursor

def sql_execute(query, fetch):
    conn = psycopg2.connect(dbname='messenger_1', user='messenger_1', password='messenger_1', host='90.189.168.29')
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    answer = None
    cursor.execute(query)
    try:
        answer = cursor.fetchall() if fetch else cursor.fetchone()
    except Exception as err:
        return err
    finally:
        conn.close()
        cursor.close
        return answer


def db_addUser(data):
    sql  = """
        INSERT INTO "User" ("first_name","last_name") 
        VALUES ({firstname},{secondname});
        INSERT INTO "Authentication" ("login","password") 
        VALUES ("{login}","{password}");
    """.format(**data)
    sql_execute(sql, True)


def db_delUser(ID, data):
    # TODO: Добавить запрос на удаление пользователя
    sql  = """
        UPDATE users 
        SET is_deleted = true 
        WHERE id = {ID};
    """.format(**)
    sql_execute(sql, True)


def db_isValidUser(data):
    sql = """
        SELECT count(id) 
        FROM "Authentication" 
        WHERE "login"={login}};
    """.format(**data)
    return sql_execute(sql, False)


def db_getProfileInfo(ID):
    sql = """
        SELECT first_name, last_name, created_at, last_visit 
        FROM "User" 
        WHERE "id"={ID};
    """.format(ID)
    return sql_execute(sql, False)


def db_updateProfileInfo(ID, data):
    if data['first_name']:
        sql = """
            UPDATE "User" 
            SET "first_name"={first_name} 
            WHERE "id"={ID};
        """.format(data['first_name'], ID)

    if data['last_name']:
        sql = """
            UPDATE "User" 
            SET "last_name"={last_name} 
            WHERE "id"={ID};
        """.format(ID)

    sql_execute(sql, False)


def db_getProfilesInfo():
    sql = """
        SELECT * 
        FROM Users;
    """
    return sql_execute(sql, False)


def db_isValidData(data):
    sql = """
        SELECT count(password) 
        FROM "Authenticaton" 
        WHERE "login"={login} 
        AND "password"={password};
    """.format(**data)
    return sql_execute(sql, False)

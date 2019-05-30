from flask import jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

def sql_execute(query, fetch):
    conn = psycopg2.connect(dbname='messenger_1', user='messenger_1', password='messenger_1', host='90.189.168.29')
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    answer = None
    cursor.execute(query)
    cursor.commit()
    try:
        answer = cursor.fetchall() if fetch else cursor.fetchone()
    except psycopg2.Error as err:
        return jsonify({'status': err})
    finally:
        conn.close()
        cursor.close
        return jsonify({'status': 1}) if not answer else jsonify(answer)



def db_addUser(data):
    sql="""
        INSERT INTO users (first_name, second_name, created_at, last_visit, is_blocked, is_active, is_deleted) 
        VALUES ({firstname}, {secondname}, NOW(), NOW(), false, true, false) RETURNING id;
    """.format(**data)
    userid = sql_execute(sql, True)
    sql = """
        INSERT INTO authentications (user_id, 'login', 'password') 
        VALUES (""" + userid + """, {login}, {password});
    """.format(**data)
    sql_execute(sql, True);


def db_delUser(ID):
    sql="""
        UPDATE users 
        SET is_deleted = true 
        WHERE id = {ID};
    """.format(ID)
    sql_execute(sql, True)


def db_isValidUser(data):
    sql="""
        SELECT count(id) 
        FROM authentication
        WHERE 'login' ={login};
    """.format(**data)
    return sql_execute(sql, False)


def db_getProfileInfo(ID):
    sql="""
        SELECT first_name, last_name, created_at, last_visit 
        FROM users
        WHERE id ={ID};
    """.format(ID)
    return sql_execute(sql, False)


def db_updateProfileInfo(ID, data):
    if data['first_name']:
        sql="""
            UPDATE users 
            SET first_name = {first_name} 
            WHERE id = {ID};
        """.format(data['first_name'], ID)

    if data['last_name']:
        sql="""
            UPDATE users 
            SET last_name = {last_name} 
            WHERE id = {ID};
        """.format(ID)

    sql_execute(sql, False)


def db_getProfilesInfo():
    sql="""
        SELECT first_name, last_name, created_at, last_visit
        FROM users;
    """
    return sql_execute(sql, False)


def db_isValidData(data):
    sql="""
        SELECT count(password) 
        FROM authenticaton 
        WHERE 'login' = {login}
        AND 'password' = {password};
    """.format(**data)
    return sql_execute(sql, False)


def db_sendMessage(data):
    sql=""""
          
    """.format(**data)


def db_getMessage(ID):
    sql="""
    """.format(ID)
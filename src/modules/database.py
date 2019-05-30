from flask import jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

def sql_execute(query, fetch=True):
    conn = psycopg2.connect(dbname='messenger_1', user='messenger_1', password='messenger_1', host='90.189.168.29')
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    answer = None
    cursor.execute(query)
    conn.commit()
    try:
        if fetch:
            answer = cursor.fetchall()
        else:
            cursor.fetchone()
    except psycopg2.Error as err:
        return jsonify({'error': err})
    finally:
        conn.close()
        cursor.close
        if not answer:
            return jsonify({'status': 1})
        else:
            return jsonify(answer)
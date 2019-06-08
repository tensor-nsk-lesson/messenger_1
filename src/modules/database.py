import psycopg2
from psycopg2.extras import RealDictCursor

def sql_execute(query, fetch_all):
    conn = psycopg2.connect(dbname='messenger_1', user='messenger_1', password='messenger_1', host='90.189.168.29')
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    answer = None
    cursor.execute(query)
    conn.commit()
    try:
        if fetch_all:
            answer = cursor.fetchall()
        else:
            answer = cursor.fetchone()
    except psycopg2.Error as err:
        '''
            Попытается зафетчить, если будет такая возможность. 
            TRUE - вернёт answer
            FALSE - скажет, что нечего возвращать
        '''
        #print(err)
        pass

    finally:
        cursor.close()
        conn.close()
        return answer
from modules.database import sql_execute;

def db_addDialog(nameDialog):
    sql='''
        INSERT INTO dialogs (name, created_at)
        VALUES ('{name}', NOW()) RETURNING id;
    '''.format(**nameDialog)
    dialogID = sql_execute(sql, fetch_all=False)
    return dialogID['id']


def db_addUserInDialog(userID, dialogID, permission):
    sql='''
        INSERT INTO dialogUser (dialog_id, user_id, permission)
        VALUES ('{:d}', '{:d}', '{:d}'})
    '''.format(dialogID, userID, permission)
    sql_execute(sql, fetch_all=False)
    return {'status': 1}


def db_addMessageForDialog(userID, content, dialogID, section_id=0):
    sql='''
        INSERT INTO messages (dialog_id, content, created_at, user_id, section_id)
        VALUES ('{:d}', '{}', NOW(), '{:d}', '{:d}')
    '''.format(dialogID, userID, section_id, content)
    sql_execute(sql, fetch_all=False)
    return {'status': 1}


def db_getMessagesFromDialog(dialogID):
    sql = '''
        SELECT user_id, content, created_at, section_id
        FROM messages
        WHERE dialog_id='{:d}'
    '''.format(dialogID)
    return sql_execute(sql, fetch_all=True)
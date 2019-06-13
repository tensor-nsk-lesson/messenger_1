from modules.API.sql_execute import sql_execute

## Chat

def db_addChat(nameChat):
    sql='''
        INSERT INTO chat (name, created_at, is_deleted)
        VALUES ('{name}', NOW(), false) 
        RETURNING id;
    '''.format(**nameChat)
    chatID = sql_execute(sql, fetch_all=False)
    return chatID['id']

def db_addUserInChat(userID, chatID, permission=0):
    sql='''
        INSERT INTO permissions_users (chat_id, user_id, permission)
        VALUES ('{:d}', '{:d}', '{:d}')
    '''.format(chatID, userID, permission)
    sql_execute(sql, fetch_all=False)
    return {'status': 1}

def db_getChat(chatID):
    sql='''
        SELECT name, created_at
        FROM chat
        WHERE id={:d}
    '''.format(chatID)
    return sql_execute(sql, True)

def db_getChatFromUser(userID, chatID):
    sql='''
        SELECT name, created_at
        FROM chat
        WHERE (
            SELECT chat_id 
            FROM permissions_users 
            WHERE user_id={:d})={:d}
    '''.format(userID, chatID)
    return sql_execute(sql, True)

def db_delChat(chatID, fully=False):
    if fully:
        sql='''
            DELETE FROM chat
            WHERE id={:d}
        '''.format(chatID)
    else:
        sql='''
            UPDATE chat
            SET is_deleted=true
            WHERE id={:d}
        '''.format(chatID)
    return sql_execute(sql, False)

## Message

def db_addMessageForChat(userID, chatID, content, section_id=0):
    sql = '''
        INSERT INTO message (context, created_at, section_id)
        VALUES ('{}', NOW(), '{:d}')
        RETURNING id;
    '''.format(content, section_id)
    messageID = sql_execute(sql, fetch_all=True)
    sql='''
        INSERT INTO messages_users (chat_id, user_id, message_id)
        VALUES ('{:d}', '{:d}', '{:d}')
    '''.format(chatID, userID, messageID)
    sql_execute(sql, fetch_all=False)
    return {'status': 1}

def db_getMessagesUserFromChat(userID, chatID):
    sql = '''
        SELECT content, created_at, section_id
        FROM messages_users, message
        WHERE user_id='{:d}' and chat_id='{:d}'
    '''.format(userID, chatID)
    return sql_execute(sql, fetch_all=True)

def db_getMessagesFromChat(chatID):
    sql = '''
        SELECT user_id, content, created_at, section_id
        FROM messages_users, message
        WHERE chat_id='{:d}'
    '''.format(chatID)
    return sql_execute(sql, fetch_all=True)

def db_updateMessage(messageID, content):
    sql='''
        UPDATE message
        SET content='{:s}' and is_edited=true
        WHERE id={:d} and section_id=0
    '''.format(content, messageID)

def db_delMessage(messageID, fully=False):
    if fully:
        sql='''
            DELETE FROM message
            WHERE id={:d}
        '''.format(messageID)
    else:
        sql='''
            UPDATE message
            SET is_deleted=true
            WHERE id={:d}
        '''.format(messageID)
    return sql_execute(sql, True)

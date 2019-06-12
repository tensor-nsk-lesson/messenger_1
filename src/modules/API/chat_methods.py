from modules.API.sql_execute import sql_execute


def db_addChat(nameChat):
    sql='''
        INSERT INTO chat (name, created_at)
        VALUES ('{name}', NOW()) RETURNING id;
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
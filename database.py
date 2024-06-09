import sqlite3


connection = sqlite3.connect('database.db', check_same_thread=False)


cursor = connection.cursor()


users = '''
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    chat_id BIGINT NOT NULL
);
'''


translations = '''
DROP TABLE IF EXISTS translations;
CREATE TABLE IF NOT EXISTS translations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lang_from TEXT,
    lang_to TEXT,
    original_text TEXT,
    translated_text TEXT,
    user_id INTEGER REFERENCES users(id)
);
'''


# cursor.executescript(users)
# cursor.executescript(translations)


def is_user_exists(chat_id):
    sql = "SELECT id FROM users WHERE chat_id=?"
    cursor.execute(sql, (chat_id, ))
    user_id = cursor.fetchone()
    if not user_id:
        return False
    return True


def add_user(first_name, chat_id):
    sql = "INSERT INTO users(first_name, chat_id) VALUES (?, ?)"
    if not is_user_exists(chat_id):
        cursor.execute(sql, (first_name, chat_id))
        connection.commit()


def add_translation(lang_from, lang_to, original_text, translated_text, chat_id):
    sql_1 = "INSERT INTO translations(lang_from, lang_to, original_text, translated_text, user_id)VALUES(?, ?, ? ,?, ?)"
    sql_2 = "SELECT id FROM users WHERE chat_id=?"
    cursor.execute(sql_2, (chat_id,))
    user_id = cursor.fetchone()[0]
    cursor.execute(sql_1, (lang_from, lang_to, original_text, translated_text, user_id))
    connection.commit()


def get_history(chat_id):
    user_sql_or = "SELECT original_text FROM translations WHERE user_id=?"
    user_sql_tr = "SELECT translated_text FROM translations WHERE user_id=?"
    or_text = cursor.fetchall()
    cursor.execute(user_sql_or, (chat_id,))
    tr_text = cursor.fetchall()
    cursor.execute(user_sql_tr, (chat_id,))
    connection.commit()


connection.commit()

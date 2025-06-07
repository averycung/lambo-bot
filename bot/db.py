import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST"),
        port=int(os.environ.get("MYSQLPORT")),
        user=os.environ.get("MYSQLUSER"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE")
    )

def add_bull(telegram_id, bref_code):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO user_codes (telegram_id, bull_ref_code) VALUES (%s, %s) ON DUPLICATE KEY UPDATE bull_ref_code = VALUES(bull_ref_code)"
    cursor.execute(query, (telegram_id, bref_code))
    conn.commit()
    cursor.close()
    conn.close()

def add_axiom(telegram_id, aref_code):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO user_codes (telegram_id, axiom_ref_code) VALUES (%s, %s) ON DUPLICATE KEY UPDATE axiom_ref_code = VALUES(axiom_ref_code)"
    cursor.execute(query, (telegram_id, aref_code))
    conn.commit()
    cursor.close()
    conn.close()

def add_username_usercodes(telegram_id, username):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO user_codes (telegram_id, username) VALUES (%s, %s) ON DUPLICATE KEY UPDATE username = VALUES(username)"
    cursor.execute(query, (telegram_id, username))
    conn.commit()
    cursor.close()
    conn.close()

def add_username_chatowners(chat_id, username):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO chat_owners (chat_id, username) VALUES (%s, %s) ON DUPLICATE KEY UPDATE username = VALUES(username)"
    cursor.execute(query, (chat_id, username))
    conn.commit()
    cursor.close()
    conn.close()

def claim_chat(xchat_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO chat_owners (chat_id, telegram_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE telegram_id = VALUES(telegram_id)"
    cursor.execute(query, (xchat_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    
def add_user(telegram_id, username):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO users (telegram_id, username) VALUES (%s, %s) ON DUPLICATE KEY UPDATE username = VALUES(username)"
    cursor.execute(query, (telegram_id, username))
    conn.commit()
    cursor.close()
    conn.close()

def view(tg_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT bull_ref_code, axiom_ref_code FROM user_codes WHERE telegram_id = %s"
    cursor.execute(query, (tg_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def delcode(tg_id, platform):
    conn = get_connection()
    cursor = conn.cursor()
    if platform == "bull_ref_code":
        query = "UPDATE user_codes SET bull_ref_code = NULL WHERE telegram_id = %s"
        cursor.execute(query, (tg_id,))
    elif platform == "axiom_ref_code":
        query = "UPDATE user_codes SET axiom_ref_code = NULL WHERE telegram_id = %s"
        cursor.execute(query, (tg_id,))
    conn.commit()
    cursor.close()
    conn.close()

def find_bull(chat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_id FROM chat_owners WHERE chat_id = %s", (chat_id,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        return None
    tgid = row[0]
    cursor.execute("SELECT bull_ref_code FROM user_codes WHERE telegram_id = %s", (tgid,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def find_ax(chat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_id FROM chat_owners WHERE chat_id = %s", (chat_id,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        return None
    tgid = row[0]
    cursor.execute("SELECT axiom_ref_code FROM user_codes WHERE telegram_id = %s", (tgid,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def find_owner(chat_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT telegram_id FROM chat_owners WHERE chat_id = %s"
    cursor.execute(query, (chat_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

import mysql.connector

conn = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),         
    port=int(os.getenv("MYSQLPORT")),    
    user=os.getenv("MYSQLUSER"),         
    password=os.getenv("MYSQLPASSWORD"), 
    database=os.getenv("MYSQLDATABASE")  
)

cursor = conn.cursor()

def add_bull(telegram_id, bref_code):
    query = "INSERT INTO user_codes (telegram_id, bull_ref_code) VALUES (%s, %s) ON DUPLICATE KEY UPDATE    bull_ref_code = VALUES (bull_ref_code)"
    values = (telegram_id, bref_code)
    cursor.execute(query, values)
    conn.commit()

def add_axiom(telegram_id, aref_code):
    query = "INSERT INTO user_codes (telegram_id, axiom_ref_code) VALUES (%s, %s) ON DUPLICATE KEY UPDATE    axiom_ref_code = VALUES (axiom_ref_code)"
    values = (telegram_id, aref_code)
    cursor.execute(query, values)
    conn.commit()

def claim_chat(xchat_id, user_id):
    query = "INSERT INTO chat_owners (chat_id, telegram_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE    telegram_id = VALUES(telegram_id)"
    values = (xchat_id, user_id)
    cursor.execute(query, values)
    conn.commit()

def view(tg_id):
    query = "SELECT bull_ref_code, axiom_ref_code FROM user_codes WHERE telegram_id = %s"
    cursor.execute(query, (tg_id,))
    result = cursor.fetchone()
    return result

def delcode(tg_id, platform):
    if platform == "bull_ref_code":
        query = "UPDATE user_codes SET bull_ref_code = NULL WHERE telegram_id = %s"
        cursor.execute(query, (tg_id,))
        conn.commit()
    elif platform == "axiom_ref_code":
        query = "UPDATE user_codes SET axiom_ref_code = NULL WHERE telegram_id = %s"
        cursor.execute(query, (tg_id,))
        conn.commit()

def find_bull(chat_id):
    query = "SELECT telegram_id FROM chat_owners WHERE chat_id = %s"
    cursor.execute(query, (chat_id,))
    tgid = cursor.fetchone()
    if tgid is None:
        return None
    tgid = tgid[0]

    query = "SELECT bull_ref_code FROM user_codes WHERE telegram_id = %s"
    cursor.execute(query, (tgid,))
    result = cursor.fetchone()
    return result[0]

def find_ax(chat_id):
    query = "SELECT telegram_id FROM chat_owners WHERE chat_id = %s"
    cursor.execute(query, (chat_id,))
    tgid = cursor.fetchone()
    if tgid is None:
        return None
    tgid = tgid[0]

    query = "SELECT axiom_ref_code FROM user_codes WHERE telegram_id = %s"
    cursor.execute(query, (tgid,))
    result = cursor.fetchone()
    return result[0]

def find_owner(chat_id):
    query = "SELECT telegram_id FROM chat_owners WHERE chat_id = %s"
    cursor.execute(query, (chat_id,))
    result = cursor.fetchone()
    return result[0]

import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_table_if_not_exists(conn, table_name):
    try:
        c = conn.cursor()
        c.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            rsi REAL,
            pair TEXT,
            time TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    except Error as e:
        print(e)
        
def insert_data(conn, rsi, time, symbol, table_name):
    try:
        c = conn.cursor()
        c.execute(f'''
                INSERT INTO {table_name} (rsi, pair, time) VALUES (?, ?, ?)
                ''', (rsi, symbol, time)) 
        conn.commit()
    except Error as e:
        print(e)
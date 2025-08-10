import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS guestbook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(name, message):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO guestbook (name, message) VALUES (?, ?)', (name, message))
    conn.commit()
    conn.close()

def get_entries():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT name, message FROM guestbook ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows

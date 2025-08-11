import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS guestbook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(name, message):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        'INSERT INTO guestbook (name, message, created_at) VALUES (?, ?, ?)',
        (name, message, created_at)
    )
    conn.commit()
    conn.close()

def get_entries():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT name, message, created_at FROM guestbook ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows

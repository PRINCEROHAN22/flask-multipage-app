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

# --- CRUD helpers ---
def get_entry(item_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT id, name, message, created_at FROM guestbook WHERE id = ?', (item_id,))
    row = c.fetchone()
    conn.close()
    return row

def update_entry(item_id, name, message):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('UPDATE guestbook SET name = ?, message = ? WHERE id = ?', (name, message, item_id))
    conn.commit()
    conn.close()

def delete_entry(item_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('DELETE FROM guestbook WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# --- Pagination + Search helpers ---
def count_entries(q=None):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    if q:
        like = f"%{q}%"
        c.execute('SELECT COUNT(*) FROM guestbook WHERE name LIKE ? OR message LIKE ?', (like, like))
    else:
        c.execute('SELECT COUNT(*) FROM guestbook')
    (count,) = c.fetchone()
    conn.close()
    return count

def get_entries_paged(page=1, limit=5, q=None):
    offset = (page - 1) * limit
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    if q:
        like = f"%{q}%"
        c.execute('''
            SELECT id, name, message, created_at
            FROM guestbook
            WHERE name LIKE ? OR message LIKE ?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        ''', (like, like, limit, offset))
    else:
        c.execute('''
            SELECT id, name, message, created_at
            FROM guestbook
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
    rows = c.fetchall()
    conn.close()
    return rows

import sqlite3

DB_NAME = "inventory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
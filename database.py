import sqlite3

def connect():
    return sqlite3.connect("users.db")

def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()
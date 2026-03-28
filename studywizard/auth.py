from database import connect
import sqlite3

def register(username, password):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()
        return True

    except sqlite3.IntegrityError:
        conn.close()
        return False


def login(username, password):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cur.fetchone()
    conn.close()

    return user is not None
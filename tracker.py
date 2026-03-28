from database import get_connection

def save_score(username, quiz_topic, score, total):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO scores (username, quiz_topic, score, total)
        VALUES (?, ?, ?, ?)
        """,
        (username, quiz_topic, score, total)
    )

    conn.commit()
    conn.close()


def get_scores(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT quiz_topic, score, total
        FROM scores
        WHERE username = ?
        ORDER BY id DESC
        """,
        (username,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows
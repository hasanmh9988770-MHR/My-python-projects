import sqlite3

DB = "quotes.db"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        author TEXT,
        sentiment TEXT,
        confidence REAL
    )
    """)

    conn.commit()
    conn.close()


def insert_quote(text, author, sentiment, confidence):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO quotes (text, author, sentiment, confidence) VALUES (?, ?, ?, ?)",
        (text, author, sentiment, confidence)
    )

    conn.commit()
    conn.close()


def get_quotes(limit=20):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM quotes ORDER BY id DESC LIMIT ?", (limit,))
    data = cur.fetchall()

    conn.close()
    return data
# ---------- db.py ----------
import sqlite3
import os

DB = "data/quotes.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Place the updated CREATE TABLE here:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT NOT NULL,
        date TEXT DEFAULT (date('now')) 
    )
    """)

    conn.commit()
    conn.close()


# ---------- INSERT QUOTE ----------
def insert_quote(text, author):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    # Adding (date('now')) manually in the INSERT statement:
    cur.execute(
        "INSERT INTO quotes (text, author, date) VALUES (?, ?, date('now'))",
        (text, author)
    )
    conn.commit()
    conn.close()


# ---------- GET ALL QUOTES ----------
def get_all_quotes():
    conn = sqlite3.connect(DB)
    # This line tells SQLite to return rows as dictionaries!
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM quotes") # Make sure your table has a 'date' column!
    rows = [dict(row) for row in cur.fetchall()]

    conn.close()
    return rows
import sqlite3
import asyncio


DB_NAME = "donat.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


async def init_db():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id INTEGER UNIQUE,
        username TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        amount REAL,
        message TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)

    conn.commit()
    conn.close()


async def add_user(user_id, username):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
        (user_id, username)
    )

    conn.commit()
    conn.close()


async def add_donation(user_id, amount, message):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO donations (user_id, amount, message)
        VALUES (?, ?, ?)
        """,
        (user_id, amount, message)
    )

    conn.commit()
    conn.close()

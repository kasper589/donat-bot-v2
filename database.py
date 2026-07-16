import sqlite3


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
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        game TEXT,
        package TEXT,
        player_id TEXT,
        amount REAL,
        currency TEXT,
        method TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)

    conn.commit()
    conn.close()


async def add_user(user_id, username):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO users
        (user_id, username)
        VALUES (?, ?)
        """,
        (user_id, username)
    )

    conn.commit()
    conn.close()


async def add_order(
    user_id,
    game,
    package,
    player_id,
    amount,
    currency,
    method
):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO orders
        (
            user_id,
            game,
            package,
            player_id,
            amount,
            currency,
            method
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            game,
            package,
            player_id,
            amount,
            currency,
            method
        )
    )

    conn.commit()
    conn.close()


async def get_users_count():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    result = cursor.fetchone()[0]

    conn.close()

    return result


async def get_orders_count():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM orders"
    )

    result = cursor.fetchone()[0]

    conn.close()

    return result

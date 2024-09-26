import sqlite3


def get_db_connection():
    conn = sqlite3.connect("Xpense.db")
    return conn


def init_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )"""
    )
    conn.commit()
    conn.close()


def init_income_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            u_id INTEGER,
            amount TEXT NOT NULL,
            source TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY (u_id) REFERENCES users(id)
        )"""
    )
    conn.commit()
    conn.close()


def init_db():
    init_users_table()
    init_income_table()


if __name__ == "__main__":
    init_db()

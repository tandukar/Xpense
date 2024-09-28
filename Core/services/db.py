import sqlite3


def get_db_connection():
    conn = sqlite3.connect("Xpense.db")
    conn.execute("PRAGMA foreign_keys = ON")
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
            income_id INTEGER PRIMARY KEY AUTOINCREMENT,
            u_id INTEGER,
            amount  REAL NOT NULL,
            source TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (u_id) REFERENCES users(id)
        )"""
    )
    conn.commit()
    conn.close()


def init_category_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            u_id INTEGER,
            category_name TEXT NOT NULL
        )"""
    )
    conn.commit()
    conn.close()


def init_budget_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS budget (
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            u_id INTEGER,
            category_id INTEGER,
            budget_limit REAL NOT NULL,
            budget_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            FOREIGN KEY (u_id) REFERENCES users(id)
            FOREIGN KEY (category_id) REFERENCES category(category_id)
        )"""
    )
    conn.commit()
    conn.close()


def init_expense_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS expense (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            u_id INTEGER,
            amount INTEGER NOT NULL,
            budget_id INTEGER,
            date TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (u_id) REFERENCES users(id),
            FOREIGN KEY (budget_id) REFERENCES budget(budget_id)
        )"""
    )
    conn.commit()
    conn.close()


def init_db():
    init_users_table()
    init_income_table()
    init_category_table()
    init_budget_table()
    init_expense_table()


if __name__ == "__main__":
    init_db()

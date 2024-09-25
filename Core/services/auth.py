# services/auth.py
import sqlite3
from hashlib import sha256


def hash_password(password):
    return sha256(password.encode("utf-8")).hexdigest()


def get_db_connection():
    conn = sqlite3.connect("Xpense.db")
    return conn


def init_db():
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


def register_service(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return {"status": "error", "message": "Username already exists!"}

    password_hash = hash_password(password)
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash),
    )
    conn.commit()
    conn.close()

    return {"status": "success", "message": "User registered successfully!"}


def validate_user_service(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (username, password_hash),
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return {"status": "success", "message": "Login successful!"}
    else:
        return {"status": "error", "message": "Invalid username or password"}

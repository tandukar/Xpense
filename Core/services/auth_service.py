from hashlib import sha256
from .db import init_db, get_db_connection


def hash_password(password):
    return sha256(password.encode("utf-8")).hexdigest()


# Initialize the database and create tables
init_db()


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

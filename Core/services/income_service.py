from .db import get_db_connection
import sqlite3


def create_income_service(u_id, amount, source, description, date):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO income (u_id, amount, source, description, date) 
            VALUES (?, ?, ?, ?, ?)""",
            (u_id, amount, source, description, date),
        )
        conn.commit()
        return {"status": "success", "message": "Income record created successfully!"}
    except sqlite3.IntegrityError as e:
        return {"status": "error", "message": f"Error occurred: {str(e)}"}
    finally:
        conn.close()

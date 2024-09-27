from .db import get_db_connection
import sqlite3


def create_expense_service(u_id, expense_amt, desc, category_id, date):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO expense (u_id, amount, description, category_id, date)
            VALUES (?, ?, ?, ?, ?)""",
            (u_id, expense_amt, desc, category_id, date),
        )
        conn.commit()
        return {"status": "success", "message": "expense record created successfully!"}
    except sqlite3.IntegrityError as e:
        return {"status": "error", "message": f"Error occurred: {str(e)}"}
    finally:
        conn.close()

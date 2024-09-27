from .db import get_db_connection
import sqlite3


def create_budget_service(
    u_id, budget_name, budget_limit, category_id, start_date, end_date
):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO budget (u_id, budget_name, budget_limit, category_id, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (u_id, budget_name, budget_limit, category_id, start_date, end_date),
        )
        conn.commit()
        return {"status": "success", "message": "Budget record created successfully!"}
    except sqlite3.IntegrityError as e:
        return {"status": "error", "message": f"Error occurred: {str(e)}"}
    finally:
        conn.close()

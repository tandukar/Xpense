from .db import get_db_connection
import sqlite3


def create_category_service(u_id, category_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO category (u_id, category_name) 
            VALUES (?, ?)""",
            (u_id, category_name),
        )
        conn.commit()
        return {"status": "success", "message": "category created successfully!"}
    except sqlite3.IntegrityError as e:
        return {"status": "error", "message": f"Error occurred: {str(e)}"}
    finally:
        conn.close()


def get_category_service(u_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM category WHERE u_id = ?", (u_id,))
        records = cursor.fetchall()

        if records:
            return {"status": "success", "data": records}
        else:
            return {"status": "success", "message": "No records found for this user."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    finally:
        conn.close()

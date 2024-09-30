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


def get_income_service(u_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM income WHERE u_id = ?", (u_id,))
        records = cursor.fetchall()

        if records:
            return {"status": "success", "data": records}
        else:
            return {"status": "success", "message": "No records found for this user."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    finally:
        conn.close()


def del_income_service(income_id, u_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM income WHERE income_id = ? AND u_id = ?", (income_id, u_id)
        )
        record = cursor.fetchone()

        if record:
            cursor.execute("DELETE FROM income WHERE income_id = ?", (income_id,))
            conn.commit()
            return {
                "status": "success",
                "message": "Income record deleted successfully.",
            }
        else:
            return {"status": "error", "message": "Record not found for this user."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    finally:
        conn.close()


def update_income_service(income_id, new_amount, new_date, u_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE income SET amount = ?, date = ? WHERE income_id = ? AND u_id = ?",
            (new_amount, new_date, income_id, u_id),
        )
        conn.commit()
        return {"status": "success", "message": "Income record updated successfully."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    finally:
        conn.close()

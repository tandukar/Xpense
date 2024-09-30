from .db import get_db_connection
import sqlite3


def create_expense_service(u_id, expense_amt, desc, category_id, date):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:  # paxi fix to real budget id
        cursor.execute(
            """INSERT INTO expense (u_id, amount, description, budget_id, date) 
            VALUES (?, ?, ?, ?, ?)""",
            (u_id, expense_amt, desc, category_id, date),
        )
        conn.commit()
        return {"status": "success", "message": "expense record created successfully!"}
    except sqlite3.IntegrityError as e:
        return {"status": "error", "message": f"Error occurred: {str(e)}"}
    finally:
        conn.close()


def get_expense_service(u_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM expense WHERE u_id = ?", (u_id,))
        records = cursor.fetchall()

        if records:
            return {"status": "success", "data": records}
        else:
            return {"status": "success", "message": "No records found for this user."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    finally:
        conn.close()


def del_expense_service(expense_id, u_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM expense WHERE expense_id = ? AND u_id = ?",
            (expense_id, u_id),
        )
        record = cursor.fetchone()

        if record:
            cursor.execute("DELETE FROM expense WHERE expense_id = ?", (expense_id,))
            conn.commit()
            return {
                "status": "success",
                "message": "expense record deleted successfully.",
            }
        else:
            return {"status": "error", "message": "Record not found for this user."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    finally:
        conn.close()


def update_expense_service(expense_id, new_amount, new_date, u_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE expense SET amount = ?, date = ? WHERE expense_id = ? AND u_id = ?",
            (new_amount, new_date, expense_id, u_id),
        )
        conn.commit()
        return {"status": "success", "message": "Expense record updated successfully."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    finally:
        conn.close()

from .db import get_db_connection


def get_expense_total(u_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Ensure u_id is a tuple
        cursor.execute(
            "SELECT sum(amount) FROM expense WHERE u_id = ?", (int(u_id),)
        )  # Convert to int
        records = cursor.fetchone()

        if records and records[0] is not None:
            return {"status": "success", "data": records[0]}
        else:
            return {"status": "success", "message": "No records found for this user."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    finally:
        conn.close()


def get_income_total(u_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Ensure u_id is a tuple
        cursor.execute(
            "SELECT sum(amount) FROM income WHERE u_id = ?", (int(u_id),)
        )  # Convert to int
        records = cursor.fetchone()

        if records and records[0] is not None:
            return {"status": "success", "data": records[0]}
        else:
            return {"status": "success", "message": "No records found for this user."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    finally:
        conn.close()

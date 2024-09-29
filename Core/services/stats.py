from .db import get_db_connection
from datetime import datetime


def get_expense_total(u_id, range):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if range == "Current Month":
            # Get the first day of the current month
            first_day_of_month = datetime.now().replace(day=1).date()
            cursor.execute(
                "SELECT sum(amount) FROM expense WHERE u_id = ? AND date >= ?",
                (int(u_id), first_day_of_month),
            )
        else:  # "All Transactions"
            cursor.execute(
                "SELECT sum(amount) FROM expense WHERE u_id = ?", (int(u_id),)
            )

        records = cursor.fetchone()

        if records and records[0] is not None:
            return {"status": "success", "data": records[0]}
        else:
            return {"status": "success", "message": "No records found for this user."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    finally:
        conn.close()


def get_income_total(u_id, range):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if range == "Current Month":
            # Get the first day of the current month
            first_day_of_month = datetime.now().replace(day=1).date()
            cursor.execute(
                "SELECT sum(amount) FROM income WHERE u_id = ? AND date >= ?",
                (int(u_id), first_day_of_month),
            )
        else:  # "All Transactions"
            cursor.execute(
                "SELECT sum(amount) FROM income WHERE u_id = ?", (int(u_id),)
            )

        records = cursor.fetchone()

        if records and records[0] is not None:
            return {"status": "success", "data": records[0]}
        else:
            return {"status": "success", "message": "No records found for this user."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    finally:
        conn.close()

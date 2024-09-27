from .db import get_db_connection
from datetime import datetime, date
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


# def get_budgets_for_current_month(u_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         # Query to get budgets for the current month
#         cursor.execute(
#             """
#             SELECT * FROM budget
#             WHERE u_id = ?
#             AND strftime('%Y-%m', start_date) = strftime('%Y-%m', 'now')
#             """,
#             (u_id,),
#         )
#         budgets = cursor.fetchall()

#         # Process the results if needed, like converting into dict format
#         budget_list = []
#         for budget in budgets:
#             budget_data = {
#                 "budget_id": budget[0],
#                 "budget_name": budget[2],
#                 "budget_limit": budget[3],
#                 "category_id": budget[4],
#                 "start_date": budget[5],
#                 "end_date": budget[6],
#             }
#             budget_list.append(budget_data)

#         return {"status": "success", "data": budget_list}

#     except sqlite3.Error as e:
#         return {"status": "error", "message": f"Database error: {str(e)}"}
#     finally:
#         conn.close()


def get_budgets_for_current_month(u_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Query to get budgets for the current month
        cursor.execute(
            """
            SELECT budget_id, budget_name, budget_limit 
            FROM budget
            WHERE u_id = ?
            AND strftime('%Y-%m', start_date) = strftime('%Y-%m', 'now')
            """,
            (u_id,),
        )
        budgets = cursor.fetchall()

        budget_list = []
        for budget in budgets:
            budget_id = budget[0]
            budget_name = budget[1]
            budget_limit = budget[2]

            # Query to get total expenses for each budget in the current month
            cursor.execute(
                """
                SELECT IFNULL(SUM(amount), 0) AS total_expense
                FROM expense
                WHERE budget_id = ?
                AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
                """,
                (budget_id,),
            )
            total_expense = cursor.fetchone()[0]

            # Calculate progress bar value as a percentage of the budget used
            progress_percentage = (
                (total_expense / budget_limit) * 100 if budget_limit > 0 else 0
            )

            budget_list.append(
                {"budget_name": budget_name, "progress_percentage": progress_percentage}
            )

        return {"status": "success", "data": budget_list}

    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    finally:
        conn.close()

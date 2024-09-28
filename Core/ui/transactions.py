from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QSettings
from services.expense_service import get_expense_service
from services.income_service import get_income_service


class Transactions(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = QLabel("Transactions Page")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        layout.addWidget(title_label)
        self.setLayout(layout)

        settings = QSettings("xpense", "xpense")
        u_id = settings.value("user_id")

        if u_id is None:
            return QMessageBox.warning(
                self, "Error", "User ID not found! Please log in again."
            )
        self.transactions(u_id, layout)

    def refresh_transactions(self):
        """Refreshes both income and expense records."""
        settings = QSettings("xpense", "xpense")
        u_id = settings.value("user_id")

        layout = self.layout()
        self.clear_layout(layout)

        if u_id:
            self.transactions(u_id, layout)

    def clear_layout(self, layout):
        """Helper function to clear all items from the layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def transactions(self, u_id, layout):
        income_response = get_income_service(u_id)
        expense_response = get_expense_service(u_id)

        # income records
        if "data" in income_response:
            income_list = income_response["data"]
            income_title = QLabel("Income")
            income_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            layout.addWidget(income_title)

            for income in income_list:
                self.transaction_row(income, layout, is_income=True)
        else:
            income_title = QLabel("No income records found.")
            income_title.setFont(QFont("Arial", 12, QFont.Weight.Normal))
            layout.addWidget(income_title)

        #  expense records
        if "data" in expense_response:
            expense_list = expense_response["data"]
            expense_title = QLabel("Expense")
            expense_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            layout.addWidget(expense_title)

            for expense in expense_list:
                self.transaction_row(expense, layout, is_income=False)
        else:
            expense_title = QLabel("No expense records found.")
            expense_title.setFont(QFont("Arial", 12, QFont.Weight.Normal))
            layout.addWidget(expense_title)

    def transaction_row(self, data, layout, is_income):
        transaction_item = QFrame()
        transaction_item.setStyleSheet(
            """
                QFrame {
                    background-color: #2a2a2a;
                    border-radius: 10px;
                    padding: 2px;
                    margin: 2px 0;
                }
            """
        )
        transaction_items_layout = QVBoxLayout(transaction_item)

        # retrieving fields from the data
        date = str(data[4])
        amt = data[2]
        date_label = QLabel(f"Date: {date}")
        date_label.setStyleSheet("color: green;" if is_income else "color: red;")
        date_label.setFont(QFont("Arial", 10, QFont.Weight.Normal))

        amt_label = QLabel(f"Rs: {amt}")
        amt_label.setStyleSheet("color: green;" if is_income else "color: red;")
        amt_label.setFont(QFont("Arial", 10, QFont.Weight.Normal))

        transaction_items_layout.addWidget(date_label)
        transaction_items_layout.addWidget(amt_label)

        layout.addWidget(transaction_item)

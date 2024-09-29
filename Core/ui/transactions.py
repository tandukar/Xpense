from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QMessageBox,
    QTreeWidget,
    QTreeWidgetItem,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QSettings
from services.expense_service import get_expense_service
from services.income_service import get_income_service
from services.utility import get_id


class Transactions(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.u_id = get_id()
        title_label = QLabel("Transactions Page")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        layout.addWidget(title_label)

        note_label = QLabel(
            "Click arrow to view detiled drop down of income and expenses"
        )
        note_label.setFont(QFont("Arial", 9, QFont.Weight.Normal))
        note_label.setStyleSheet("font-style: italic;")
        layout.addWidget(note_label)
        # Create the tree widget with styling
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Transaction Type", "Date", "Amount"])
        self.tree_widget.setStyleSheet(
            """
            QTreeWidget {
                background-color: #2a2a2a;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #3a3a3a;
                color: white;
                font-weight: bold;
                padding: 5px;
            }
            QTreeWidgetItem {
                background-color: #2a2a2a;
            }
            QTreeWidget::item {
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                margin: 2px 0;
            }
            """
        )
        layout.addWidget(self.tree_widget)
        self.setLayout(layout)

        if self.u_id is None:
            return QMessageBox.warning(
                self, "Error", "User ID not found! Please log in again."
            )
        self.transactions(self.u_id)

    def refresh_transactions(self):  # this refreshes both records

        self.clear_tree()

        if self.u_id:
            self.transactions(self.u_id)

    def clear_tree(self):
        self.tree_widget.clear()

    def transactions(self, u_id):
        income_response = get_income_service(u_id)
        expense_response = get_expense_service(u_id)

        # Handle income records
        if "data" in income_response:
            income_list = income_response["data"]
            income_item = QTreeWidgetItem(self.tree_widget, ["Income", "", ""])
            income_item.setBackground(
                0, Qt.GlobalColor.green
            )  # Set background for the Income header
            for income in income_list:
                self.add_transaction_item(income, income_item, is_income=True)

        # Handle expense records
        if "data" in expense_response:
            expense_list = expense_response["data"]
            expense_item = QTreeWidgetItem(self.tree_widget, ["Expense", "", ""])
            expense_item.setBackground(
                0, Qt.GlobalColor.red
            )  # Set background for the Expense header
            for expense in expense_list:
                self.add_transaction_item(expense, expense_item, is_income=False)

    def add_transaction_item(self, data, parent_item, is_income):
        # Retrieve fields from the data
        date = str(data[4])  # Adjust index according to your data structure
        amt = data[2]

        # Create a child item for each transaction
        transaction_item = QTreeWidgetItem(parent_item, ["", date, f"Rs: {amt}"])
        transaction_item.setText(0, "Income" if is_income else "Expense")

        # Set text color based on transaction type
        transaction_item.setForeground(
            0, Qt.GlobalColor.green if is_income else Qt.GlobalColor.red
        )
        transaction_item.setForeground(1, Qt.GlobalColor.white)
        transaction_item.setForeground(2, Qt.GlobalColor.white)

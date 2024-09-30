from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QMessageBox,
    QTreeWidget,
    QTreeWidgetItem,
    QMenu,
    QLineEdit,
    QPushButton,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal
from services.expense_service import (
    get_expense_service,
    del_expense_service,
    update_expense_service,
)
from services.income_service import (
    get_income_service,
    del_income_service,
    update_income_service,
)
from services.utility import get_id


class Transactions(QWidget):
    transaction_updated = pyqtSignal()

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
        note_label2 = QLabel(
            "Right Click on an item inside the treeview to update it or delete it."
        )
        note_label.setFont(QFont("Arial", 9, QFont.Weight.Normal))
        note_label.setStyleSheet("font-style: italic;")
        layout.addWidget(note_label)
        note_label2.setFont(QFont("Arial", 9, QFont.Weight.Normal))
        note_label2.setStyleSheet("font-style: italic;")
        layout.addWidget(note_label2)
        # Tree Widget
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

        # setting up context menus
        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.open_menu)

    def open_menu(self, position):
        item = self.tree_widget.itemAt(position)
        if item and item.parent():
            menu = QMenu()
            edit_action = menu.addAction("Edit")
            delete_action = menu.addAction("Delete")
            action = menu.exec(self.tree_widget.viewport().mapToGlobal(position))

            if action == edit_action:
                self.update_transaction(item)
            elif action == delete_action:
                self.delete_transaction(item)

    def update_transaction(self, item):
        # Retrieve current values
        current_date = item.text(1)
        current_amount = item.text(2)
        transaction_type = item.text(0)
        transaction_id = item.data(0, Qt.ItemDataRole.UserRole)
        u_id = self.u_id  #

        modal = QWidget()
        modal.setWindowTitle("Edit Transaction")

        layout = QVBoxLayout()

        date_input = QLineEdit(modal)
        date_input.setPlaceholderText("Enter new date")
        date_input.setText(current_date)

        amount_input = QLineEdit(modal)
        amount_input.setPlaceholderText("Enter new amount")
        amount_input.setText(current_amount)

        update_button = QPushButton("Update", modal)

        layout.addWidget(date_input)
        layout.addWidget(amount_input)
        layout.addWidget(update_button)

        modal.setLayout(layout)

        def on_update():
            new_date = date_input.text()
            new_amount = amount_input.text()
            if new_date and new_amount:
                # Updating the database based on transaction type
                if transaction_type == "Income":
                    result = update_income_service(
                        transaction_id, new_amount, new_date, u_id
                    )
                else:
                    result = update_expense_service(
                        transaction_id, new_amount, new_date, u_id
                    )

                if result["status"] == "success":
                    # this updates the treeview ui
                    item.setText(1, new_date)
                    item.setText(2, new_amount)
                    QMessageBox.information(modal, "Success", result["message"])
                    modal.close()
                    self.transaction_updated.emit()
                else:
                    QMessageBox.warning(modal, "Error", result["message"])
            else:
                QMessageBox.warning(modal, "Error", "Please fill in both fields.")

        update_button.clicked.connect(on_update)

        modal.show()

    def delete_transaction(self, item):
        response = QMessageBox.question(
            self,
            "Delete Transaction",
            "Are you sure you want to delete this transaction?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if response == QMessageBox.StandardButton.Yes:

            transaction_type = item.text(0)  #
            transaction_id = item.data(0, Qt.ItemDataRole.UserRole)
            u_id = self.u_id

            if transaction_type == "Income":
                result = del_income_service(transaction_id, u_id)
            else:
                result = del_expense_service(transaction_id, u_id)

            if result["status"] == "success":
                parent = item.parent()
                if parent:
                    parent.removeChild(item)  # Remove the item from the treeview
                self.tree_widget.takeTopLevelItem(
                    self.tree_widget.indexOfTopLevelItem(item)
                )

                QMessageBox.information(self, "Deleted", result["message"])
                self.transaction_updated.emit()
            else:
                QMessageBox.warning(self, "Error", result["message"])

    def refresh_transactions(self):
        # this refreshes both data
        self.clear_tree()
        if self.u_id:
            self.transactions(self.u_id)

    def clear_tree(self):
        self.tree_widget.clear()

    def transactions(self, u_id):
        income_response = get_income_service(u_id)
        expense_response = get_expense_service(u_id)

        # Handle income
        if "data" in income_response:
            income_list = income_response["data"]
            income_item = QTreeWidgetItem(self.tree_widget, ["Income", "", ""])
            income_item.setBackground(0, Qt.GlobalColor.green)
            for income in income_list:
                self.add_transaction_item(income, income_item, is_income=True)

        # Handle expense
        if "data" in expense_response:
            expense_list = expense_response["data"]
            expense_item = QTreeWidgetItem(self.tree_widget, ["Expense", "", ""])
            expense_item.setBackground(0, Qt.GlobalColor.red)
            for expense in expense_list:
                self.add_transaction_item(expense, expense_item, is_income=False)

    def add_transaction_item(self, data, parent_item, is_income):
        date = str(data[4])
        amt = data[2]
        income_id = data[0]
        # print(f"Adding Income ID: {income_id} (Type: {type(income_id)})")
        transaction_item = QTreeWidgetItem(parent_item, ["", date, f"{amt}"])
        transaction_item.setText(0, "Income" if is_income else "Expense")

        # Store the id as an integer
        transaction_item.setData(0, Qt.ItemDataRole.UserRole, income_id)

        transaction_item.setForeground(
            0, Qt.GlobalColor.green if is_income else Qt.GlobalColor.red
        )
        transaction_item.setForeground(1, Qt.GlobalColor.white)
        transaction_item.setForeground(2, Qt.GlobalColor.white)

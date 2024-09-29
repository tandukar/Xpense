from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from services.stats import get_expense_total, get_income_total
from services.utility import get_id


class Dashboard(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.u_id = get_id()
        print(self.u_id)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Welcome label
        welcome_label = QLabel("Welcome to Xpense")
        welcome_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(welcome_label, alignment=Qt.AlignmentFlag.AlignTop)

        total_layout = self.total()

        layout.addLayout(total_layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)

    def total(self):

        expense_result = get_expense_total(self.u_id)
        income_result = get_income_total(self.u_id)

        if expense_result["status"] == "success":
            expense_label = QLabel(f"Total Expenses: ${expense_result['data']:.2f}")
        else:
            expense_label = QLabel(expense_result["message"])

        if income_result["status"] == "success":
            income_label = QLabel(f"Total Income: ${income_result['data']:.2f}")
        else:
            income_label = QLabel(income_result["message"])

        total_layout = QHBoxLayout()

        expense_frame = QFrame()
        income_frame = QFrame()

        expense_frame.setStyleSheet(
            "border-radius: 10px; padding: 10px; background-color: #4CAF50; font-size:20px;"
        )
        income_frame.setStyleSheet(
            "border-radius: 10px; padding: 10px; background-color: #D37091; font-size:20px;"
        )

        expense_layout = QVBoxLayout()
        income_layout = QVBoxLayout()

        expense_layout.addWidget(expense_label)
        income_layout.addWidget(income_label)

        expense_frame.setLayout(expense_layout)
        income_frame.setLayout(income_layout)

        total_layout.addWidget(expense_frame)
        total_layout.addWidget(income_frame)

        return total_layout

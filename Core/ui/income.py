from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDateEdit,
    QTextEdit,
    QPushButton,
    QWidget,
    QFormLayout,
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from .common_widgets import CommonInput, CommonDate, CommonButton


class Income(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel("Add Income")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(title_label)

        # Wrapper widget for form layout (with grey background)
        form_container = QWidget()
        form_container.setStyleSheet(
            """
            QWidget {
                background-color: #2a2a2a;  
                border-radius: 10px;
                padding: 15px;
            }
        """
        )

        # Form Layout for input fields inside the form_container
        income_form = QFormLayout(form_container)

        # Amount Input Field
        self.amt_input = CommonInput("Enter amount (e.g. NPR 1000)")
        amount_label = QLabel("Amount:")
        income_form.addRow(amount_label, self.amt_input)

        # Income Source Input Field
        self.income_source = CommonInput("Enter income source (e.g. Salary)")
        income_label = QLabel("Income Source:")
        income_form.addRow(income_label, self.income_source)

        # Description Input Field
        self.desc = CommonInput("Optional description")
        desc_label = QLabel("Description:")
        income_form.addRow(desc_label, self.desc)

        # Date Input Field
        self.date_input = CommonDate()
        # self.date_input.setDate(QDate.currentDate())
        # self.date_input.setFixedWidth(300)
        # self.date_input.setStyleSheet(self.common_date())
        income_form.addRow("Date:", self.date_input)

        # Add form container to main layout
        layout.addWidget(form_container)

        # Submit Button (outside the grey form section)
        submit_button = CommonButton("Add Income")
        layout.addWidget(submit_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Add some stretch to bottom layout
        layout.addStretch()

        # Set layout
        self.setLayout(layout)

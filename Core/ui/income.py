from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QWidget,
    QFormLayout,
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from .common_widgets import CommonInput, CommonDate, CommonButton, CommonNumInput


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

        income_form = QFormLayout(form_container)

        # Amount Input Field
        self.amt_input = CommonNumInput("Enter amount (e.g. NPR 1000)")
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
        income_form.addRow("Date:", self.date_input)

        # Add form container to main layout
        layout.addWidget(form_container)

        submit_button = CommonButton("Add Income")
        submit_button.clicked.connect(self.handle_submit)
        layout.addWidget(submit_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addStretch()

        self.setLayout(layout)

    def handle_submit(self):
        # retrieving input values
        amt_input = self.amt_input.text()
        income_source = self.income_source.text()
        desc = self.desc.text()
        date_input = self.date_input.date()

        if not amt_input or not income_source or not date_input:
            return QMessageBox.warning(self, "Error", "Please enter all fields!")

        print(f"Budget Name: {amt_input}")
        print(f"Budget Limit: {income_source}")
        print(f"desc: {desc}")
        print(f"Start Date: {date_input.toString(Qt.DateFormat.ISODate)}")

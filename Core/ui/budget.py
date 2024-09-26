from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QWidget,
    QFormLayout,
    QComboBox,
    QHBoxLayout,
    QMessageBox,
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from .common_widgets import (
    CommonInput,
    CommonDate,
    CommonButton,
    CommonButton2,
    CommonComboBox,
    CommonNumInput,
)
from .category_modal import CategoryModal


class Budget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel("Create Budget")
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

        budget_form = QFormLayout(form_container)

        # Budget Input Field
        self.budget_name = CommonInput("Enter Budget name")
        amount_label = QLabel("Budget name:")
        budget_form.addRow(amount_label, self.budget_name)

        # udget Limit Input Field
        self.budget_limit = CommonNumInput("Enter Budget Limit")
        income_label = QLabel("Budget Limit")
        budget_form.addRow(income_label, self.budget_limit)

        # category Input Field
        category_items = ["Option 1", "Option 2", "Option 3"]
        self.category = CommonComboBox(category_items)
        budget_form.addRow("Category:", self.category)

        # Date range
        self.start_date_input = CommonDate()
        budget_form.addRow("Start date:", self.start_date_input)
        self.end_date_input = CommonDate()
        budget_form.addRow("End date:", self.end_date_input)

        layout.addWidget(form_container)

        # buttons
        button_layout = QHBoxLayout()
        submit_button = CommonButton("Create Category")
        button_layout.addWidget(submit_button)

        submit_button2 = CommonButton2("Create Budget")
        button_layout.addWidget(submit_button2)

        # connect btn handlers
        submit_button.clicked.connect(self.open_category_modal)
        submit_button2.clicked.connect(self.handle_budget_submit)

        layout.addLayout(button_layout)
        layout.setAlignment(button_layout, Qt.AlignmentFlag.AlignRight)
        layout.addStretch()

        self.setLayout(layout)

    def open_category_modal(self):
        modal = CategoryModal(self)
        modal.exec()

    def handle_budget_submit(self):
        # retrieving input values
        budget_name = self.budget_name.text()
        budget_limit = self.budget_limit.text()
        category = self.category.currentText()
        start_date = self.start_date_input.date()
        end_date = self.end_date_input.date()

        if (
            not budget_name
            or not budget_limit
            or not category
            or not start_date
            or not end_date
        ):
            return QMessageBox.warning(self, "Error", "Please enter all fields!")

        print(f"Budget Name: {budget_name}")
        print(f"Budget Limit: {budget_limit}")
        print(f"Category: {category}")
        print(f"Start Date: {start_date.toString(Qt.DateFormat.ISODate)}")
        print(f"End Date: {end_date.toString(Qt.DateFormat.ISODate)}")

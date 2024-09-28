from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QWidget,
    QFormLayout,
    QComboBox,
    QHBoxLayout,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QDate, QSettings, pyqtSignal
from PyQt6.QtGui import QFont
from .common_widgets import (
    CommonInput,
    CommonDate,
    CommonButton,
    CommonComboBox,
    CommonNumInput,
)
from .category_modal import CategoryModal
from services.category_service import get_category_service
from services.expense_service import create_expense_service
from services.utility import CategoryUtility


class Expense(QWidget):
    expense_created = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
        self.category_utility = CategoryUtility()
        self.category_utility.load_categories(self.category)

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel("Create Expense")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(title_label)

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

        # Expense amt Field
        self.expense_amt = CommonNumInput("Enter Expense amt")
        income_label = QLabel("Expense Amount")
        budget_form.addRow(income_label, self.expense_amt)

        # category Input Field
        self.category = CommonComboBox([])
        budget_form.addRow("Category:", self.category)

        # Date range
        self.date_input = CommonDate()
        budget_form.addRow("Start date:", self.date_input)

        # desciptionField
        self.desc = CommonInput("Enter Description(optional)")
        desc_label = QLabel("Description:")
        budget_form.addRow(desc_label, self.desc)

        layout.addWidget(form_container)

        # buttons
        button_layout = QHBoxLayout()

        submit_button2 = CommonButton("Create Expense")
        button_layout.addWidget(submit_button2)

        # connect btn handlers
        submit_button2.clicked.connect(self.handle_submit)

        layout.addLayout(button_layout)
        layout.setAlignment(button_layout, Qt.AlignmentFlag.AlignRight)
        layout.addStretch()

        self.setLayout(layout)

    def handle_submit(self):
        # retrieving input values
        desc = self.desc.text().strip()
        expense_amt = self.expense_amt.text().strip()
        category_name = self.category.currentText()
        category_id = self.category_utility.get_category_id(category_name)

        date = self.date_input.date()
        date = date.toString(Qt.DateFormat.ISODate)

        if not expense_amt or not category_id or not date:
            return QMessageBox.warning(self, "Error", "Please enter all fields!")

        if int(expense_amt) < 0:
            return QMessageBox.warning(
                self, "Error", "Please enter a valid Expense amt (0 or higher)."
            )

        # If all validations pass, proceed with expense creation
        settings = QSettings("xpense", "xpense")
        u_id = settings.value("user_id")

        if u_id is None:
            return QMessageBox.warning(
                self, "Error", "User ID not found! Please log in again."
            )

        response = create_expense_service(u_id, expense_amt, desc, category_id, date)
        QMessageBox.information(self, "Expense recorded", response["message"])

        self.expense_created.emit()

        # Clear fields after its saved in db
        self.desc.clear()
        self.expense_amt.clear()
        self.category.setCurrentIndex(0)
        self.date_input.setDate(QDate.currentDate())

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QWidget,
    QFormLayout,
    QComboBox,
    QHBoxLayout,
    QMessageBox,
    QProgressBar,
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
from PyQt6.QtCore import QSettings
from services.category_service import get_category_service
from services.budget_service import (
    create_budget_service,
    get_budgets_for_current_month,
)


class Budget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_id_map = {}
        self.budget_list_layout = None  # To store layout for current month budgets
        self.initUI()
        self.load_categories()
        self.load_current_month_budgets()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel("Create Budget")
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

        # Budget Input Field
        self.budget_name = CommonInput("Enter Budget name")
        amount_label = QLabel("Budget name:")
        budget_form.addRow(amount_label, self.budget_name)

        # Budget Limit Input Field
        self.budget_limit = CommonNumInput("Enter Budget Limit")
        income_label = QLabel("Budget Limit")
        budget_form.addRow(income_label, self.budget_limit)

        # Category Input Field
        self.category = CommonComboBox([])
        budget_form.addRow("Category:", self.category)

        # Date range
        self.start_date_input = CommonDate()
        budget_form.addRow("Start date:", self.start_date_input)
        self.end_date_input = CommonDate()
        budget_form.addRow("End date:", self.end_date_input)

        layout.addWidget(form_container)

        # Buttons
        button_layout = QHBoxLayout()
        submit_button = CommonButton("Create Category")
        button_layout.addWidget(submit_button)

        submit_button2 = CommonButton2("Create Budget")
        button_layout.addWidget(submit_button2)

        # Connect button handlers
        submit_button.clicked.connect(self.open_category_modal)
        submit_button2.clicked.connect(self.handle_budget_submit)

        layout.addLayout(button_layout)
        layout.setAlignment(button_layout, Qt.AlignmentFlag.AlignRight)

        # Current Month Budgets Section
        self.budget_list_layout = (
            QVBoxLayout()
        )  # Layout for showing current month budgets
        layout.addLayout(self.budget_list_layout)

        self.setLayout(layout)

    def load_current_month_budgets(self):
        # Function to retrieve and display current month budgets
        settings = QSettings("xpense", "xpense")
        u_id = settings.value("user_id")

        if u_id is None:
            QMessageBox.warning(
                self, "Error", "User ID not found! Please log in again."
            )
            return

        response = get_budgets_for_current_month(u_id)

        if response["status"] == "success":
            budgets = response.get("data", [])
            self.update_budget_list(budgets)
        else:
            QMessageBox.warning(self, "Error", response["message"])

    def update_budget_list(self, budgets):
        # Clear the layout before updating
        while self.budget_list_layout.count():
            item = self.budget_list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        if not budgets:
            no_budgets_label = QLabel("No budgets found for this month.")
            self.budget_list_layout.addWidget(no_budgets_label)
        else:
            for budget in budgets:
                budget_name = budget["budget_name"]
                progress_percentage = budget["progress_percentage"]

                # Create label for budget name
                budget_label = QLabel(f"{budget_name}:")
                budget_label.setStyleSheet("color: white; font-size: 14px;")

                # Create progress bar for budget
                progress_bar = QProgressBar()
                progress_bar.setValue(int(progress_percentage))
                progress_bar.setStyleSheet(
                    """
                    QProgressBar {
                        border: 1px solid #555555;
                        border-radius: 5px;
                        background-color: #2a2a2a;
                    }
                    QProgressBar::chunk {
                        background-color: #00bfff;
                    }
                    """
                )
                progress_bar.setFormat(f"{progress_percentage:.2f}%")

                # Add label and progress bar to the layout
                self.budget_list_layout.addWidget(budget_label)
                self.budget_list_layout.addWidget(progress_bar)

    def open_category_modal(self):
        modal = CategoryModal(self)
        modal.exec()

    def handle_budget_submit(self):
        # Retrieving input values
        budget_name = self.budget_name.text().strip()
        budget_limit = self.budget_limit.text().strip()
        category_name = self.category.currentText()
        category_id = self.category_id_map.get(category_name)
        start_date = self.start_date_input.date()
        end_date = self.end_date_input.date()
        start_date = start_date.toString(Qt.DateFormat.ISODate)
        end_date = end_date.toString(Qt.DateFormat.ISODate)

        if (
            not budget_name
            or not budget_limit
            or not category_id
            or not start_date
            or not end_date
        ):
            return QMessageBox.warning(self, "Error", "Please enter all fields!")

        if int(budget_limit) < 0:
            return QMessageBox.warning(
                self, "Error", "Please enter a valid budget limit (0 or higher)."
            )

        if start_date >= end_date:
            return QMessageBox.warning(
                self, "Error", "End date must be after start date."
            )

        # If all validations pass, proceed with budget creation
        settings = QSettings("xpense", "xpense")
        u_id = settings.value("user_id")

        if u_id is None:
            return QMessageBox.warning(
                self, "Error", "User ID not found! Please log in again."
            )

        response = create_budget_service(
            u_id, budget_name, budget_limit, category_id, start_date, end_date
        )
        QMessageBox.information(self, "Budget Submission", response["message"])

        # Clear fields after it's saved in db
        self.budget_name.clear()
        self.budget_limit.clear()
        self.category.setCurrentIndex(0)
        self.start_date_input.setDate(QDate.currentDate())
        self.end_date_input.setDate(QDate.currentDate())

    def load_categories(self):
        settings = QSettings("xpense", "xpense")
        u_id = settings.value("user_id")

        if u_id is None:
            QMessageBox.warning(
                self, "Error", "User ID not found! Please log in again."
            )
            return

        response = get_category_service(u_id)

        if response["status"] == "success":
            categories = response.get("data", [])
            if categories:
                self.category.clear()
                self.category_id_map.clear()  # Clear the existing map
                for category in categories:
                    category_id, category_name = (
                        category[0],
                        category[2],
                    )  # Use ID and name
                    self.category.addItem(category_name)
                    self.category_id_map[category_name] = category_id  # Map name to ID
        else:
            QMessageBox.warning(self, "Error", response["message"])

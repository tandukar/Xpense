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
from PyQt6.QtCore import QDate, pyqtSignal
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
from services.utility import CategoryUtility


class Budget(QWidget):
    budget_created = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_id_map = {}
        self.budget_list_layout = None  # To store layout for current month budgets
        self.initUI()
        self.load_current_month_budgets()
        self.category_utility = CategoryUtility()
        self.category_utility.load_categories(self.category)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        title_label = QLabel("Create Budget")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label
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

        # budget field
        self.budget_name = CommonInput("Enter Budget name")
        amount_label = QLabel("Budget name:")
        budget_form.addRow(amount_label, self.budget_name)

        # limit field
        self.budget_limit = CommonNumInput("Enter Budget Limit")
        income_label = QLabel("Budget Limit")
        budget_form.addRow(income_label, self.budget_limit)

        self.category = CommonComboBox([])
        budget_form.addRow("Category:", self.category)

        # date range
        self.start_date_input = CommonDate()
        budget_form.addRow("Start date:", self.start_date_input)
        self.end_date_input = CommonDate()
        budget_form.addRow("End date:", self.end_date_input)

        layout.addWidget(form_container)

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

        # budget Section (of the currrent month)
        list_title_label = QLabel()
        list_title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        # Apply rich text formatting to change only "current month" to italic and smaller
        list_title_label.setText(
            'Budget Usage (<span style="font-size:12pt; font-style:italic;">current month</span>)'
        )

        layout.addWidget(list_title_label)

        self.budget_list_layout = QVBoxLayout()
        layout.addLayout(self.budget_list_layout)

        self.setLayout(layout)

    def connect_expense_signal(self, expense):
        expense.expense_created.connect(self.load_current_month_budgets)

    def load_current_month_budgets(
        self,
    ):  # get budget to calcutate rate of expense of the budget
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
            no_budgets_label.setStyleSheet("color: white; font-size: 14px;")
            self.budget_list_layout.addWidget(no_budgets_label)
        else:
            for budget in budgets:
                budget_name = budget["budget_name"]
                percentage = budget["percentage"]
                exceeded = budget["exceeded"]

                # Create a horizontal layout for each budget item
                budget_item_layout = QHBoxLayout()

                # Budget name label
                budget_label = QLabel(f"{budget_name}:")
                budget_label.setStyleSheet("color: white; font-size: 14px;")
                budget_item_layout.addWidget(budget_label)

                # Progress bar
                progress_bar = QProgressBar()
                progress_bar.setRange(0, 100)
                progress_bar.setValue(
                    min(int(percentage), 100)
                )  # Cap the visual fill at 100%
                progress_bar.setFormat(f"{percentage:.2f}%")
                progress_bar.setFixedWidth(200)

                if exceeded:
                    progress_bar.setStyleSheet(
                        """
                        QProgressBar {
                            border: 1px solid #555555;
                            border-radius: 5px;
                            background-color: #2a2a2a;
                            color: white;
                            text-align: center;
                        }
                        QProgressBar::chunk {
                            background-color: #ff0000;
                        }
                    """
                    )
                else:
                    progress_bar.setStyleSheet(
                        """
                        QProgressBar {
                            border: 1px solid #555555;
                            border-radius: 5px;
                            background-color: #2a2a2a;
                            color: white;
                            text-align: center;
                        }
                        QProgressBar::chunk {
                            background-color: #253aba;
                        }
                    """
                    )
                budget_item_layout.addWidget(progress_bar)

                # Exceeded label
                if exceeded:
                    exceeded_label = QLabel("EXCEEDED")
                    exceeded_label.setStyleSheet(
                        "color: #ff0000; font-weight: bold; font-size: 14px;"
                    )
                    budget_item_layout.addWidget(exceeded_label)

                # Add some stretch to push everything to the left
                budget_item_layout.addStretch()

                # Add the horizontal layout to the main vertical layout
                self.budget_list_layout.addLayout(budget_item_layout)

    def open_category_modal(self):
        modal = CategoryModal(self)
        modal.exec()
        self.category_utility.load_categories(self.category)

    def handle_budget_submit(self):
        # Retrieving input values
        budget_name = self.budget_name.text().strip()
        budget_limit = self.budget_limit.text().strip()
        category_name = self.category.currentText()
        # category_id = self.category_id_map.get(category_name)
        category_id = self.category_utility.get_category_id(category_name)
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
            print(budget_name)
            print(budget_limit)
            print(category_id)
            print(start_date)
            print(end_date)
            return QMessageBox.warning(self, "Error", "Please enter all fields!")

        if int(budget_limit) < 0:
            return QMessageBox.warning(
                self, "Error", "Please enter a valid budget limit (0 or higher)."
            )

        if start_date >= end_date:
            return QMessageBox.warning(
                self, "Error", "End date must be after start date."
            )

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

        self.budget_created.emit()
        # Clear fields after it's saved in db
        self.budget_name.clear()
        self.budget_limit.clear()
        self.category.setCurrentIndex(0)
        self.start_date_input.setDate(QDate.currentDate())
        self.end_date_input.setDate(QDate.currentDate())
        self.load_current_month_budgets()

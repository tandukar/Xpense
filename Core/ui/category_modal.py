from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QListWidget,
    QHBoxLayout,
    QMessageBox,
)
from services.category_service import create_category_service, get_category_service
from .common_widgets import (
    CommonInput,
    CommonButton,
)
from PyQt6.QtCore import QSettings


class CategoryModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Category")
        self.setFixedSize(400, 300)

        self.layout = QVBoxLayout()

        self.category_field_layout = QHBoxLayout()
        self.category_input = CommonInput("Enter category name")
        self.category_field_layout.addWidget(self.category_input)

        self.add_button = CommonButton("Add Category")
        self.add_button.clicked.connect(self.handle_submit)
        self.category_field_layout.addWidget(self.add_button)
        self.layout.addLayout(self.category_field_layout)

        # retrieve from db
        self.category_list = QListWidget()
        self.layout.addWidget(self.category_list)

        self.setLayout(self.layout)
        self.load_categories()

    def handle_submit(self):
        category_name = self.category_input.text().strip()
        if not category_name:
            QMessageBox.warning(self, "Error", "Category name cannot be empty!")
            return

        settings = QSettings("xpense", "xpense")
        u_id = settings.value("user_id")

        if u_id is None:
            return QMessageBox.warning(
                self, "Error", "User ID not found! Please log in again."
            )

        # income service
        response = create_category_service(u_id, category_name)

        QMessageBox.information(self, "Income Submission", response["message"])

        # db ma save garni,esko satta
        self.category_list.addItem(category_name)
        self.category_input.clear()

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
                self.category_list.clear()
                for category in categories:
                    self.category_list.addItem(category[2])
        else:
            QMessageBox.warning(self, "Error", response["message"])

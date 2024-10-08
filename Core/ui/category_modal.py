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
from PyQt6.QtCore import pyqtSignal
from services.utility import get_id


class CategoryModal(QDialog):
    category_created = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Category")
        self.setFixedSize(400, 300)
        self.u_id = get_id()
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

        if self.u_id is None:
            return QMessageBox.warning(
                self, "Error", "User ID not found! Please log in again."
            )

        # category service
        response = create_category_service(self.u_id, category_name)
        self.category_created.emit()
        QMessageBox.information(self, "category Submission", response["message"])

        self.category_list.addItem(category_name)
        self.category_input.clear()

    def load_categories(self):

        if self.u_id is None:
            QMessageBox.warning(
                self, "Error", "User ID not found! Please log in again."
            )
            return

        response = get_category_service(self.u_id)

        if response["status"] == "success":
            categories = response.get("data", [])
            if categories:
                self.category_list.clear()
                for category in categories:
                    self.category_list.addItem(category[2])
        else:
            QMessageBox.warning(self, "Error", response["message"])

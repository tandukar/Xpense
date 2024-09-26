from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QHBoxLayout,
    QMessageBox,
)

from .common_widgets import (
    CommonInput,
    CommonDate,
    CommonButton,
    CommonButton2,
    CommonComboBox,
    CommonNumInput,
)


class CategoryModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Category")
        self.setFixedSize(400, 300)

        self.layout = QVBoxLayout()

        # Input field for new category
        self.category_field_layout = QHBoxLayout()
        self.category_input = CommonInput("Enter category name")
        self.category_field_layout.addWidget(self.category_input)

        # Button to add category
        self.add_button = CommonButton("Add Category")
        self.add_button.clicked.connect(self.add_category)
        self.category_field_layout.addWidget(self.add_button)
        self.layout.addLayout(self.category_field_layout)

        # List to show existing categories
        self.category_list = QListWidget()
        self.layout.addWidget(self.category_list)

        self.setLayout(self.layout)

    def add_category(self):
        category_name = self.category_input.text().strip()
        if not category_name:
            QMessageBox.warning(self, "Error", "Category name cannot be empty!")
            return

        # Here you could add code to save the category to the database
        # For now, we just add it to the list
        self.category_list.addItem(category_name)
        self.category_input.clear()

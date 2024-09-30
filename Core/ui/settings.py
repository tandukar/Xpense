from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpacerItem, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from .common_widgets import AuthButton, CommonInput
from services.auth_service import change_password, logout_user
from services.utility import get_id


class Settings(QWidget):
    def __init__(self, switch_to_login, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.u_id = get_id()
        self.switch_to_login = switch_to_login
        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()

        # Title for the Settings page
        title_label = QLabel("Settings")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(title_label)

        # Add space (margin top) between title and sections
        layout.addSpacerItem(QSpacerItem(20, 40))

        profile_label = QLabel("User Profile Settings")
        profile_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(profile_label)

        layout.addSpacerItem(QSpacerItem(20, 20))

        # Label for password section
        password_label = QLabel("Change Password")
        password_label.setFont(QFont("Arial", 12))
        layout.addWidget(password_label)

        self.old_pwd = CommonInput("Old Password", is_password=True)
        self.old_pwd.setFixedWidth(300)
        layout.addWidget(self.old_pwd)

        self.new_pwd = CommonInput("New Password", is_password=True)
        self.new_pwd.setFixedWidth(300)
        layout.addWidget(self.new_pwd)

        self.new_pwd2 = CommonInput("Confirm New Password", is_password=True)
        self.new_pwd2.setFixedWidth(300)
        layout.addWidget(self.new_pwd2)

        layout.addSpacerItem(QSpacerItem(5, 5))

        # Create the change password button
        save_btn = AuthButton("Confirm New Password")
        save_btn.setFixedWidth(300)
        save_btn.clicked.connect(
            self.change_password
        )  # Connect button to change_password method
        layout.addWidget(save_btn)

        # Add stretch to push the button to the top
        layout.addStretch()
        self.setLayout(layout)

    def change_password(self):
        old_password = self.old_pwd.text()
        new_password = self.new_pwd.text()
        confirm_password = self.new_pwd2.text()

        if not old_password or not new_password or not confirm_password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Input Error", "New passwords do not match.")
            return

        if new_password == old_password:
            QMessageBox.warning(
                self, "Input Error", "New password is the same as the old one"
            )
            return

        result = change_password(self.u_id, old_password, new_password)
        QMessageBox.information(self, "Result", result["message"])

        # Clear the input fields after operation
        self.old_pwd.clear()
        self.new_pwd.clear()
        self.new_pwd2.clear()

        logout_user()
        self.switch_to_login()

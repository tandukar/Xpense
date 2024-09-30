from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from .common_widgets import AuthButton, AuthInput


class Settings(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()


from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class Settings(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

        self.old_pwd = AuthInput("Old Password", is_password=True)
        layout.addWidget(self.old_pwd)
        self.new_pwd = AuthInput("New Password", is_password=True)
        layout.addWidget(self.new_pwd)
        self.new_pwd2 = AuthInput("Old Password", is_password=True)
        layout.addWidget(self.new_pwd2)
        layout.addSpacerItem(QSpacerItem(5, 5))
        save_btn = AuthButton("Confirm New Password")
        save_btn.setFixedWidth(300)

        layout.addWidget(save_btn)

        # Add stretch to push the button to the top
        layout.addStretch()
        self.setLayout(layout)

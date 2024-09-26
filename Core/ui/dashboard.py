from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class Dashboard(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to Xpense Dashboard")
        welcome_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        welcome_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        layout.addWidget(welcome_label)
        layout.addStretch()
        self.setLayout(layout)

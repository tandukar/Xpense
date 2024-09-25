from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Dashboard(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("Welcome to Xpense ")

        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        label.setFont(font)

        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(label)

        layout.addStretch()  # This will push the label to the top

        self.setLayout(layout)

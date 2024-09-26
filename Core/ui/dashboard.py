from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor


class Dashboard(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # sidebar
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #2a2a2a;")
        sidebar.setFixedWidth(180)
        sidebar_layout = QVBoxLayout()
        sidebar_title = QLabel("Xpense")
        sidebar_title.setStyleSheet("color: #ffffff; padding: 5px;  ")
        sidebar_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sidebar_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        sidebar_layout.addWidget(sidebar_title)

        sidebar_items = [
            "Dashboard",
            "Transactions",
            "Budget",
            " Statistics",
            "Settings",
        ]
        for item in sidebar_items:
            btn = QPushButton(item)
            btn.setStyleSheet(
                """
                QPushButton {
                    color: white; 
                    padding: 10px; 
                    border: none; 
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #3949AB;
                }
            """
            )
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)

        render_page = QFrame()
        render_page_layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to Xpense")
        font = QFont("Arial", 20, QFont.Weight.Bold)
        welcome_label.setFont(font)
        welcome_label.setStyleSheet("color: white;")
        welcome_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        render_page_layout.addWidget(welcome_label)
        render_page_layout.addStretch()  # This pushes the welcome message to the top
        render_page.setLayout(render_page_layout)

        # layout.addWidget(label)
        layout.addWidget(sidebar)
        layout.addWidget(render_page)
        layout.addStretch()  # This will push the label to the top

        self.setLayout(layout)

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QStackedWidget,
    QWidget,
    QPushButton,
)
from PyQt6 import QtGui
from ui.dashboard import Dashboard
from ui.auth import Login, Register
from services.auth_service import init_db


class XpenseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("./assets/logo.jpg"))
        self.setWindowTitle("Xpense")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        init_db()  # Initialize the database

        # Create the stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize authentication screens
        self.login = Login(self.show_register, self.switch_dashboard)
        self.register = Register(self.show_login)

        self.dashboard = Dashboard()  # The dashboard will contain the navbar

        # Add screens to the stacked widget
        self.stacked_widget.addWidget(self.login)
        self.stacked_widget.addWidget(self.register)
        self.stacked_widget.addWidget(self.dashboard)

        # Show the login screen first
        self.stacked_widget.setCurrentWidget(self.login)

    def show_register(self):
        self.stacked_widget.setCurrentWidget(self.register)

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login)

    def switch_dashboard(self):
        self.stacked_widget.setCurrentWidget(self.dashboard)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = XpenseApp()
    window.show()
    sys.exit(app.exec())

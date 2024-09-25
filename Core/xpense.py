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


class XpenseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("./assets/logo.jpg"))
        self.setWindowTitle("Xpense")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize authentication screens
        self.login = Login(self.show_register)
        self.register = Register(self.show_login)

        self.stacked_widget.addWidget(self.login)
        self.stacked_widget.addWidget(self.register)

        # Show login screen initially
        self.stacked_widget.setCurrentWidget(self.login)

    def show_register(self):
        self.stacked_widget.setCurrentWidget(self.register)

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = XpenseApp()
    window.show()
    sys.exit(app.exec())

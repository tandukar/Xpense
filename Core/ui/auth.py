from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFrame,
)
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt
from .common_widgets import AuthInput, AuthButton


class BaseAuthScreen(QWidget):
    """
    Base class for shared functionalities between Login and Register screens.
    """

    def __init__(self):
        super().__init__()

    def create_frame(self, title):
        """
        for creating a frame with a title label.
        :return: QFrame and its layout
        """
        frame = QFrame(self)
        frame.setStyleSheet(
            "background-color: #2a2a2a; border-radius: 10px; padding: 20px;"
        )
        frame.setFixedWidth(300)
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 24))
        title_label.setStyleSheet("color: #ffffff;")
        frame_layout.addWidget(title_label)

        return frame, frame_layout

    def create_link_label(self, text, slot):
        """
        Creates a label with a hyperlink to switch between login and register.
        :param text: Text for the label with HTML anchor tag
        :param slot: Slot function to be triggered on link click
        :return: QLabel
        """
        link_label = QLabel(text)
        link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        link_label.setStyleSheet(
            "QLabel { color: #ffffff; } QLabel a { color: #007bff; text-decoration: none; }"
        )
        link_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        link_label.linkActivated.connect(slot)
        return link_label

    def validate_input(self, *inputs):
        """
        Validates that all input fields are filled.
        :param inputs: Input fields to be validated
        :return: bool, True if all inputs are filled, else False
        """
        for input_field in inputs:
            if not input_field.text():
                return False
        return True


class Login(BaseAuthScreen):
    def __init__(self, switch_register):
        super().__init__()
        self.switch_register = switch_register
        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI for the Login screen.
        """
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame, frame_layout = self.create_frame("Login")
        main_layout.addWidget(frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.username_input = AuthInput("Username")
        self.password_input = AuthInput("Password", is_password=True)
        frame_layout.addWidget(self.username_input)
        frame_layout.addWidget(self.password_input)

        login_button = AuthButton("Login")
        login_button.clicked.connect(self.login)
        frame_layout.addWidget(login_button)

        register_label = self.create_link_label(
            "Don't have an account? <a href='#'>Sign up</a>", self.switch_register
        )
        main_layout.addWidget(register_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setWindowTitle("Login")
        self.resize(400, 400)

    def login(self):
        """
        Login logic when the Login button is clicked.
        """
        if self.validate_input(self.username_input, self.password_input):
            QMessageBox.information(self, "Success", "Login successful!")
        else:
            QMessageBox.warning(
                self, "Error", "Please enter both username and password."
            )


class Register(BaseAuthScreen):
    def __init__(self, switch_login):
        super().__init__()
        self.switch_login = switch_login
        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI for the Register screen.
        """
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame, frame_layout = self.create_frame("Register")
        main_layout.addWidget(frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.username_input = AuthInput("Username")
        self.password_input = AuthInput("Password", is_password=True)
        self.confirm_password_input = AuthInput("Confirm Password", is_password=True)

        frame_layout.addWidget(self.username_input)
        frame_layout.addWidget(self.password_input)
        frame_layout.addWidget(self.confirm_password_input)

        register_button = AuthButton("Register")
        register_button.clicked.connect(self.register)
        frame_layout.addWidget(register_button)

        login_label = self.create_link_label(
            "Already have an account? <a href='#'>Log in</a>", self.switch_login
        )
        main_layout.addWidget(login_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setWindowTitle("Register")
        self.resize(400, 400)

    def register(self):
        """
        Registration logic when the Register button is clicked.
        """
        if self.validate_input(
            self.username_input, self.password_input, self.confirm_password_input
        ):
            if self.password_input.text() == self.confirm_password_input.text():
                QMessageBox.information(self, "Success", "Registration successful!")
            else:
                QMessageBox.warning(self, "Error", "Passwords do not match.")
        else:
            QMessageBox.warning(self, "Error", "Please fill all fields.")

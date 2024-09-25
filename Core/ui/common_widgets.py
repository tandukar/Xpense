from PyQt6.QtWidgets import QLineEdit, QPushButton


class AuthInput(QLineEdit):
    def __init__(self, placeholder_text, is_password=False):
        super().__init__()
        self.setPlaceholderText(placeholder_text)
        self.setMinimumWidth(200)
        self.setStyleSheet(
            "padding: 2px 6px; font-size: 14px; background-color: #444444; "
            "color: #ffffff; border: 1px solid #555555; border-radius: 5px;"
        )
        if is_password:
            self.setEchoMode(QLineEdit.EchoMode.Password)


class AuthButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet(
            "background-color: #3949AB; color: white;padding: 4px 6px; "
            "font-size: 16px; border: none; border-radius: 5px;"
        )

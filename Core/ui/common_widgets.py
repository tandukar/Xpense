from PyQt6.QtWidgets import QLineEdit, QPushButton, QDateEdit, QComboBox
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIntValidator


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


class CommonInput(QLineEdit):
    def __init__(self, placeholder_text, is_password=False):
        super().__init__()
        self.setPlaceholderText(placeholder_text)
        self.setFixedWidth(300)
        self.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #3d3d3d;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                background-color: #444444;
                color: white;
            }
            QLineEdit:hover {
                border: 2px solid #3949AB;
            }
            """
        )

        if is_password:
            self.setEchoMode(QLineEdit.EchoMode.Password)


class CommonNumInput(QLineEdit):
    def __init__(self, placeholder_text):
        super().__init__()
        self.setPlaceholderText(placeholder_text)
        self.setFixedWidth(300)

        # this validates to allow only integers
        int_validator = QIntValidator(self)
        self.setValidator(int_validator)

        self.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #3d3d3d;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                background-color: #444444;
                color: white;
            }
            QLineEdit:hover {
                border: 2px solid #3949AB;
            }
            """
        )


class CommonComboBox(QComboBox):
    def __init__(self, items):
        super().__init__()
        self.addItems(items)
        self.setPlaceholderText("Select Category")
        self.setFixedWidth(300)
        self.setStyleSheet(
            """
            QComboBox {
                border: 2px solid #3d3d3d;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                background-color: #444444;
                color: white;
            }
            QComboBox:hover {
                border: 2px solid #3949AB;
            }
            """
        )


class CommonDate(QDateEdit):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)
        self.setDate(QDate.currentDate())
        self.setStyleSheet(
            """
           QDateEdit {
            border: 2px solid #3d3d3d;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
            background-color: #444444;
            color: white;
        }

        QDateEdit:hover {
            border: 2px solid #3949AB;
        }


        """
        )


class CommonButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedWidth(130)
        self.setStyleSheet(
            """
        QPushButton {
            background-color: #3949AB;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #253aba;
        }
        """
        )


class CommonButton2(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedWidth(130)
        self.setStyleSheet(
            """
        QPushButton {
            background-color: #253aba;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #3949AB;
        }
        """
        )

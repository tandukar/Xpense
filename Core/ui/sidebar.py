from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor


class Sidebar(QFrame):
    def __init__(self, on_page_change, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_page_change = on_page_change
        self.buttons = {}
        self.current_page = None
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #2a2a2a;")
        self.setFixedWidth(180)

        sidebar_layout = QVBoxLayout()

        sidebar_title = QLabel("Xpense")
        sidebar_title.setStyleSheet("color: #ffffff; padding: 10px;")
        sidebar_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sidebar_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        sidebar_layout.addWidget(sidebar_title)

        sidebar_items = [
            ("Dashboard", "dashboard"),
            ("Income", "income"),
            ("Expense ", "expense"),
            ("Budget", "budget"),
            ("Transactions", "transactions"),
            ("Settings", "settings"),
        ]

        #  buttons and store references
        for item_name, page_name in sidebar_items:
            btn = QPushButton(item_name)
            btn.setStyleSheet(self.default_button_style())
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            # Storing the button reference
            self.buttons[page_name] = btn

            if page_name == "dashboard":
                btn.clicked.connect(self.handle_dashboard_click)
            elif page_name == "budget":
                btn.clicked.connect(self.handle_budget_click)
            elif page_name == "transactions":
                btn.clicked.connect(self.handle_transactions_click)
            elif page_name == "settings":
                btn.clicked.connect(self.handle_settings_click)
            elif page_name == "income":
                btn.clicked.connect(self.handle_income_click)
            elif page_name == "expense":
                btn.clicked.connect(self.handle_expense_click)

            sidebar_layout.addWidget(btn)

        self.set_active_button("dashboard")  # dashboard is active by default

        sidebar_layout.addStretch()
        self.setLayout(sidebar_layout)

    def default_button_style(self):
        return """
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

    def active_button_style(self):
        return """
            QPushButton {
                color: white;
                padding: 10px;
                border: none;
                text-align: left;
                background-color: #3949AB;  /* Active color */
            }
        """

    def set_active_button(self, page_name):
        # Reset the previous active button style
        if self.current_page and self.current_page in self.buttons:
            self.buttons[self.current_page].setStyleSheet(self.default_button_style())

        # Set the new active button style
        if page_name in self.buttons:
            self.buttons[page_name].setStyleSheet(self.active_button_style())
            self.current_page = page_name

    # Methods to handle page change
    def handle_dashboard_click(self):
        self.on_page_change("dashboard")
        self.set_active_button("dashboard")

    def handle_budget_click(self):
        self.on_page_change("budget")
        self.set_active_button("budget")

    def handle_transactions_click(self):
        self.on_page_change("transactions")
        self.set_active_button("transactions")

    def handle_settings_click(self):
        self.on_page_change("settings")
        self.set_active_button("settings")

    def handle_income_click(self):
        self.on_page_change("income")
        self.set_active_button("income")

    def handle_expense_click(self):
        self.on_page_change("expense")
        self.set_active_button("expense")

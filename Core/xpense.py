import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QWidget,
)
from PyQt6 import QtGui
from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.budget import Budget
from ui.settings import Settings
from ui.transactions import Transactions
from ui.income import Income
from ui.expense import Expense
from ui.auth import Login, Register
from services.auth_service import init_db


class Xpense(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("./assets/logo.jpg"))
        self.setWindowTitle("Xpense")
        self.setGeometry(100, 100, 1100, 800)
        self.setStyleSheet("background-color: #171717; color: white;")
        self.initUI()

    def initUI(self):
        init_db()  # db initialization

        self.main = QWidget(self)
        self.setCentralWidget(self.main)

        self.main_layout = QHBoxLayout(self.main)

        self.stacked_widget = QStackedWidget()

        # Initialize auth page
        self.login = Login(self.show_register, self.switch_dashboard)
        self.register = Register(self.show_login)

        # Add auth pags to  stacked widget
        self.stacked_widget.addWidget(self.login)
        self.stacked_widget.addWidget(self.register)

        # Add the stacked widget (for auth pages) to the layout, without sidebar initially
        self.main_layout.addWidget(self.stacked_widget)

        # login page is displayed initially
        self.stacked_widget.setCurrentWidget(self.login)

        # Side bar is set to none because it will only be loaded after login
        self.sidebar = None

    def show_register(self):
        self.stacked_widget.setCurrentWidget(self.register)

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login)

    def switch_login(self):
        self.stacked_widget.setCurrentWidget(self.login)
        if self.sidebar:
            self.main_layout.removeWidget(self.sidebar)
            self.sidebar.deleteLater()
            self.sidebar = None

    def switch_dashboard(self):
        # after successfull login load sidebar and  dashboard
        if not self.sidebar:
            # insert it into the layout on the left using index 0
            self.sidebar = Sidebar(self.switch_page)
            self.main_layout.insertWidget(0, self.sidebar)

        # initialize  pges and adding them to the stacked widget
        self.dashboard = Dashboard()
        self.budget = Budget()
        self.transactions = Transactions()
        self.settings = Settings(self.switch_login)
        self.income = Income()
        self.expense = Expense()

        self.budget.connect_expense_signal(self.expense)

        self.expense.connect_budget_signal(self.budget)
        self.income.income_created.connect(self.transactions.refresh_transactions)
        self.expense.expense_created.connect(self.transactions.refresh_transactions)
        self.income.income_created.connect(self.dashboard.refresh_dashboard)
        self.expense.expense_created.connect(self.dashboard.refresh_dashboard)

        self.transactions.transaction_updated.connect(self.dashboard.refresh_dashboard)
        self.transactions.transaction_updated.connect(self.dashboard.refresh_dashboard)

        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.budget)
        self.stacked_widget.addWidget(self.settings)
        self.stacked_widget.addWidget(self.transactions)
        self.stacked_widget.addWidget(self.income)
        self.stacked_widget.addWidget(self.expense)

        # after successful login dashboard is displayed
        self.stacked_widget.setCurrentWidget(self.dashboard)

    def switch_page(self, page_name):
        if page_name == "dashboard":
            self.stacked_widget.setCurrentWidget(self.dashboard)
        elif page_name == "budget":
            self.stacked_widget.setCurrentWidget(self.budget)
        elif page_name == "transactions":
            self.stacked_widget.setCurrentWidget(self.transactions)
        elif page_name == "settings":
            self.stacked_widget.setCurrentWidget(self.settings)
        elif page_name == "income":
            self.stacked_widget.setCurrentWidget(self.income)
        elif page_name == "expense":
            self.stacked_widget.setCurrentWidget(self.expense)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Xpense()
    window.show()
    sys.exit(app.exec())

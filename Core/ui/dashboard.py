from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from services.stats import get_expense_total, get_income_total
from services.utility import get_id
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class Dashboard(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pie_canvas = None
        self.line_canvas = None
        self.expense_label = None
        self.income_label = None
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        self.u_id = get_id()
        welcome_label = QLabel("Welcome to Xpense")
        welcome_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.layout.addWidget(welcome_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Total layout
        self.total_layout = QHBoxLayout()
        self.total_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.total_layout)

        # Chart layout
        chart_label = QLabel("Statistics")
        chart_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        self.layout.addWidget(chart_label, alignment=Qt.AlignmentFlag.AlignTop)
        self.chart_layout = QHBoxLayout()
        self.chart_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.chart_layout)

        # Initialize both total and chart
        self.refresh_dashboard()
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def refresh_dashboard(self):
        # refresh data when signal is caught
        self.update_totals()
        self.update_combined_chart()

    def update_totals(self):
        # Clear previous data
        if self.expense_label:
            self.expense_label.deleteLater()
        if self.income_label:
            self.income_label.deleteLater()

        expense_result = get_expense_total(self.u_id)
        income_result = get_income_total(self.u_id)

        # Set updated data
        if expense_result.get("status") == "success" and "data" in expense_result:
            self.expense_label = QLabel(
                f"Total Expenses: ${expense_result['data']:.2f}"
            )
        else:
            self.expense_label = QLabel(
                expense_result.get("message", "Error fetching expense data")
            )

        if income_result.get("status") == "success" and "data" in income_result:
            self.income_label = QLabel(f"Total Income: ${income_result['data']:.2f}")
        else:
            self.income_label = QLabel(
                income_result.get("message", "Error fetching income data")
            )

        self.expense_label.setStyleSheet(
            "border-radius: 10px; padding: 10px; background-color: #D37091; font-size:20px;"
        )
        self.income_label.setStyleSheet(
            "border-radius: 10px; padding: 10px; background-color: #4CAF50; font-size:20px;"
        )
        self.total_layout.addWidget(self.income_label)
        self.total_layout.addWidget(self.expense_label)

    def update_combined_chart(self):
        # Clear previous data
        if self.pie_canvas:
            self.pie_canvas.deleteLater()
        if self.line_canvas:
            self.line_canvas.deleteLater()

        # recreate pie and line charts
        self.pie_canvas, self.line_canvas = self.create_combined_chart()

        self.chart_layout.addWidget(self.pie_canvas)
        self.chart_layout.addWidget(self.line_canvas)

    def create_combined_chart(self):
        # Fetch  data
        expense_result = get_expense_total(self.u_id)
        income_result = get_income_total(self.u_id)

        # reetrieve expense and income values
        expense = (
            expense_result.get("data", 0)
            if expense_result.get("status") == "success"
            else 0
        )
        income = (
            income_result.get("data", 0)
            if income_result.get("status") == "success"
            else 0
        )

        # pie chart data preparation
        labels = ["Expenses", "Income"]
        values = [expense, income]
        colors = ["#D37091", "#4CAF50"]

        # this creates pie chart figure
        fig1, ax1 = plt.subplots(figsize=(2, 2))

        if sum(values) > 0:
            ax1.pie(
                values, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90
            )
            ax1.axis("equal")
            ax1.set_title("Income vs Expenses")
        else:
            ax1.text(0.5, 0.5, "No data to display", ha="center", va="center")
            ax1.axis("off")

        pie_canvas = FigureCanvas(fig1)

        # this creates line chart figure
        fig2, ax1 = plt.subplots(figsize=(3, 3))

        # Sample data for line chart (for demonstration)
        periods = ["Wk-1", "Wk-2", "Wk-3", "Wk-4"]
        income_data = [100, 150, 200, income]
        expense_data = [80, 120, 180, expense]

        # Plot expenses on the primary y-axis
        ax1.plot(periods, expense_data, label="Expenses", color="#D37091", marker="o")
        ax1.set_ylabel("Expenses ($)", color="#D37091")
        ax1.set_xlabel("Time")
        ax1.set_title("Income and Expenses Over Time")
        ax1.grid(True)

        # Set the y-axis
        max_value = max(expense_data + income_data)
        ax1.set_ylim(0, max_value + 5000)  # Set a max-limit

        # Create a second y-axis for income
        ax2 = ax1.twinx()
        ax2.plot(periods, income_data, label="Income", color="#4CAF50", marker="o")
        ax2.set_ylabel("Income ($)", color="#4CAF50")

        ax2.set_ylim(0, max_value + 5000)

        fig2.tight_layout()

        line_canvas = FigureCanvas(fig2)

        return pie_canvas, line_canvas

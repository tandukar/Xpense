from services.category_service import get_category_service
from services.budget_service import get_budgets_service
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import (
    QMessageBox,
)


class CategoryUtility:
    def __init__(self):
        self.category_id_map = {}

    def load_categories(self, category_combobox):
        settings = QSettings("xpense", "xpense")
        u_id = settings.value("user_id")

        if u_id is None:
            QMessageBox.warning(
                category_combobox, "Error", "User ID not found! Please log in again."
            )
            return

        response = get_category_service(u_id)

        if response["status"] == "success":
            categories = response.get("data", [])
            if categories:
                category_combobox.clear()
                self.category_id_map.clear()
                for category in categories:
                    category_id, category_name = (
                        category[0],
                        category[2],
                    )
                    category_combobox.addItem(category_name)
                    self.category_id_map[category_name] = category_id  # Map name to ID
        else:
            QMessageBox.warning(category_combobox, "Error", response["message"])

    def get_category_id(self, category_name):
        return self.category_id_map.get(category_name)


class BudgetUtility:
    def __init__(self):
        self.budget_id_map = {}

    def load_budgets(self, budget_combobox):
        settings = QSettings("xpense", "xpense")
        u_id = settings.value("user_id")

        if u_id is None:
            QMessageBox.warning(
                budget_combobox, "Error", "User ID not found! Please log in again."
            )
            return

        response = get_budgets_service(u_id)

        if response["status"] == "success":
            budgets = response.get("data", [])
            if budgets:
                budget_combobox.clear()
                self.budget_id_map.clear()
                for budget in budgets:
                    budget_id, budget_name = (
                        budget[0],
                        budget[4],
                    )
                    budget_combobox.addItem(budget_name)
                    self.budget_id_map[budget_name] = budget_id  # Map name to ID
        else:
            QMessageBox.warning(budget_combobox, "Error", response["message"])

    def get_budget_id(self, budget_name):
        return self.budget_id_map.get(budget_name)

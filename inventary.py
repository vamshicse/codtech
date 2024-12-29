from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
import sys


class InventorySystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inventory = {}  # Dictionary to store product details
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("background-color: #f0f8ff;")

        self.layout = QVBoxLayout()

        # Title Label
        self.titleLabel = QLabel("Inventory Management System")
        self.titleLabel.setFont(QFont("Arial", 18, QFont.Bold))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("color: #4682B4; margin: 10px;")
        self.layout.addWidget(self.titleLabel)

        # Buttons
        self.addButton = QPushButton("Add Product")
        self.editButton = QPushButton("Edit Product")
        self.deleteButton = QPushButton("Delete Product")
        self.viewButton = QPushButton("View Inventory")
        self.reportButton = QPushButton("Generate Low Stock Report")

        # Set button styles
        buttons = [self.addButton, self.editButton, self.deleteButton, self.viewButton, self.reportButton]
        for button in buttons:
            button.setFont(QFont("Arial", 12))
            button.setStyleSheet("background-color: #87CEFA; color: white; padding: 10px; margin: 5px;")
            self.layout.addWidget(button)

        # Connect buttons to functions
        self.addButton.clicked.connect(self.add_product)
        self.editButton.clicked.connect(self.edit_product)
        self.deleteButton.clicked.connect(self.delete_product)
        self.viewButton.clicked.connect(self.view_inventory)
        self.reportButton.clicked.connect(self.generate_report)

        # Central Widget
        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

    def add_product(self):
        name, ok = QInputDialog.getText(self, "Add Product", "Enter product name:")
        if ok and name:
            if name in self.inventory:
                QMessageBox.warning(self, "Error", "Product already exists.")
                return
            try:
                quantity, ok1 = QInputDialog.getInt(self, "Add Product", "Enter quantity:")
                if not ok1:
                    return
                price, ok2 = QInputDialog.getDouble(self, "Add Product", "Enter price:")
                if not ok2:
                    return
                self.inventory[name] = {"quantity": quantity, "price": price}
                QMessageBox.information(self, "Success", f"Product '{name}' added.")
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid input for quantity or price.")

    def edit_product(self):
        name, ok = QInputDialog.getText(self, "Edit Product", "Enter product name to edit:")
        if ok and name:
            if name not in self.inventory:
                QMessageBox.warning(self, "Error", "Product not found.")
                return
            try:
                quantity, ok1 = QInputDialog.getInt(self, "Edit Product", "Enter new quantity:")
                if not ok1:
                    return
                price, ok2 = QInputDialog.getDouble(self, "Edit Product", "Enter new price:")
                if not ok2:
                    return
                self.inventory[name] = {"quantity": quantity, "price": price}
                QMessageBox.information(self, "Success", f"Product '{name}' updated.")
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid input for quantity or price.")

    def delete_product(self):
        name, ok = QInputDialog.getText(self, "Delete Product", "Enter product name to delete:")
        if ok and name:
            if name in self.inventory:
                del self.inventory[name]
                QMessageBox.information(self, "Success", f"Product '{name}' deleted.")
            else:
                QMessageBox.warning(self, "Error", "Product not found.")

    def view_inventory(self):
        if not self.inventory:
            QMessageBox.information(self, "Inventory", "No products in inventory.")
            return

        inventory_window = QTableWidget()
        inventory_window.setColumnCount(3)
        inventory_window.setHorizontalHeaderLabels(["Product", "Quantity", "Price"])
        inventory_window.setRowCount(len(self.inventory))
        inventory_window.setStyleSheet("background-color: #FAFAD2;")

        for i, (name, details) in enumerate(self.inventory.items()):
            inventory_window.setItem(i, 0, QTableWidgetItem(name))
            inventory_window.setItem(i, 1, QTableWidgetItem(str(details["quantity"])))
            inventory_window.setItem(i, 2, QTableWidgetItem(f"${details['price']}"))

        inventory_window.setWindowTitle("Inventory List")
        inventory_window.resize(500, 400)
        inventory_window.show()
        self.inventory_window = inventory_window  # Prevent window from closing

    def generate_report(self):
        low_stock_threshold = 5
        low_stock_items = [
            name for name, details in self.inventory.items()
            if details["quantity"] < low_stock_threshold
        ]
        if low_stock_items:
            QMessageBox.information(
                self, "Low Stock Report",
                "Products low in stock:\n" + "\n".join(low_stock_items)
            )
        else:
            QMessageBox.information(self, "Low Stock Report", "All products are sufficiently stocked.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventorySystem()
    window.show()
    sys.exit(app.exec_())

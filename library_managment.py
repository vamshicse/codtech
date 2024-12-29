import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLineEdit, QDialog, QMessageBox, QWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Main Window Class
class LibraryManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 800, 600)

        # Data storage
        self.library_items = []  # Stores all library items as dictionaries
        self.fines = {}  # Overdue fines tracker

        # GUI Setup
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Library Management System")
        title.setFont(QFont("Arial", 24))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Buttons for functionalities
        button_add = QPushButton("Add New Item")
        button_add.clicked.connect(self.add_item)
        layout.addWidget(button_add)

        button_checkout = QPushButton("Check Out Item")
        button_checkout.clicked.connect(self.checkout_item)
        layout.addWidget(button_checkout)

        button_return = QPushButton("Return Item")
        button_return.clicked.connect(self.return_item)
        layout.addWidget(button_return)

        button_search = QPushButton("Search Library")
        button_search.clicked.connect(self.search_item)
        layout.addWidget(button_search)

        button_view = QPushButton("View All Items")
        button_view.clicked.connect(self.view_inventory)
        layout.addWidget(button_view)

        button_fines = QPushButton("Manage Overdue Fines")
        button_fines.clicked.connect(self.view_fines)
        layout.addWidget(button_fines)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_item(self):
        dialog = ItemDialog(self, "Add New Item")
        if dialog.exec_() == QDialog.Accepted:
            self.library_items.append(dialog.get_data())
            QMessageBox.information(self, "Success", "Item added successfully!")

    def checkout_item(self):
        name, ok = QInputDialog.getText(self, "Check Out Item", "Enter item title:")
        if ok and name.strip():
            for item in self.library_items:
                if item["title"].lower() == name.strip().lower() and not item.get("checked_out"):
                    item["checked_out"] = True
                    QMessageBox.information(self, "Success", f"Item '{name}' checked out!")
                    return
            QMessageBox.warning(self, "Error", f"Item '{name}' not available or already checked out.")

    def return_item(self):
        name, ok = QInputDialog.getText(self, "Return Item", "Enter item title:")
        if ok and name.strip():
            for item in self.library_items:
                if item["title"].lower() == name.strip().lower() and item.get("checked_out"):
                    item["checked_out"] = False
                    QMessageBox.information(self, "Success", f"Item '{name}' returned!")
                    return
            QMessageBox.warning(self, "Error", f"Item '{name}' not checked out.")

    def search_item(self):
        term, ok = QInputDialog.getText(self, "Search Library", "Enter title, author, or category:")
        if ok and term.strip():
            results = [
                item for item in self.library_items
                if term.strip().lower() in (item["title"] + item["author"] + item["category"]).lower()
            ]
            if results:
                self.show_results(results)
            else:
                QMessageBox.information(self, "No Results", "No items matched your search.")

    def view_inventory(self):
        if self.library_items:
            self.show_results(self.library_items)
        else:
            QMessageBox.information(self, "Empty Library", "No items in the library.")

    def view_fines(self):
        if self.fines:
            fine_details = "\n".join(f"{user}: ₹{fine}" for user, fine in self.fines.items())
            QMessageBox.information(self, "Overdue Fines", fine_details)
        else:
            QMessageBox.information(self, "No Fines", "No overdue fines to display.")

    def show_results(self, results):
        dialog = ResultsDialog(self, results)
        dialog.exec_()


# Dialog for Adding or Editing Items
class ItemDialog(QDialog):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(300, 200, 400, 300)

        layout = QVBoxLayout()

        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("Title")
        layout.addWidget(self.input_title)

        self.input_author = QLineEdit()
        self.input_author.setPlaceholderText("Author")
        layout.addWidget(self.input_author)

        self.input_category = QLineEdit()
        self.input_category.setPlaceholderText("Category")
        layout.addWidget(self.input_category)

        self.input_quantity = QLineEdit()
        self.input_quantity.setPlaceholderText("Quantity")
        layout.addWidget(self.input_quantity)

        button_save = QPushButton("Save")
        button_save.clicked.connect(self.save_data)
        layout.addWidget(button_save)

        self.setLayout(layout)

    def save_data(self):
        title = self.input_title.text().strip()
        author = self.input_author.text().strip()
        category = self.input_category.text().strip()
        quantity = self.input_quantity.text().strip()

        if not title or not author or not category or not quantity.isdigit():
            QMessageBox.warning(self, "Error", "Please enter valid data.")
            return

        self.data = {
            "title": title,
            "author": author,
            "category": category,
            "quantity": int(quantity),
            "checked_out": False
        }
        self.accept()

    def get_data(self):
        return self.data


# Dialog for Displaying Results
class ResultsDialog(QDialog):
    def __init__(self, parent, results):
        super().__init__(parent)
        self.setWindowTitle("Search Results")
        self.setGeometry(300, 200, 600, 400)

        layout = QVBoxLayout()

        table = QTableWidget(len(results), 4)
        table.setHorizontalHeaderLabels(["Title", "Author", "Category", "Checked Out"])
        for row, item in enumerate(results):
            table.setItem(row, 0, QTableWidgetItem(item["title"]))
            table.setItem(row, 1, QTableWidgetItem(item["author"]))
            table.setItem(row, 2, QTableWidgetItem(item["category"]))
            table.setItem(row, 3, QTableWidgetItem("Yes" if item.get("checked_out") else "No"))
        layout.addWidget(table)

        self.setLayout(layout)


# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryManagementSystem()
    window.show()
    sys.exit(app.exec_())

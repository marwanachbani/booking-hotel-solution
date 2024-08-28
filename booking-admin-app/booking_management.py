import sys
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QMessageBox
import requests

class BookingManagementWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()

        self.token = token
        self.setWindowTitle("Manage Bookings")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.booking_list = QListWidget()
        layout.addWidget(self.booking_list)

        self.refresh_button = QPushButton("Refresh Bookings")
        self.refresh_button.clicked.connect(self.load_bookings)
        layout.addWidget(self.refresh_button)

        self.accept_button = QPushButton("Accept Selected Booking")
        self.accept_button.clicked.connect(self.accept_booking)
        layout.addWidget(self.accept_button)

        self.deny_button = QPushButton("Deny Selected Booking")
        self.deny_button.clicked.connect(self.deny_booking)
        layout.addWidget(self.deny_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_bookings(self):
        try:
            response = requests.get("http://localhost:8000/bookings")
            if response.status_code == 200:
                bookings = response.json()
                self.booking_list.clear()
                for booking in bookings:
                    self.booking_list.addItem(f"Booking {booking['booking_id']} for Hotel {booking['hotel_id']}")
            else:
                QMessageBox.warning(self, "Error", "Failed to load bookings.")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def accept_booking(self):
        selected_item = self.booking_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "No booking selected.")
            return

        booking_id = selected_item.text().split(" ")[1]

        try:
            response = requests.post(
                f"http://localhost:8000/bookings/{booking_id}/accept",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Booking accepted!")
                self.load_bookings()
            else:
                QMessageBox.warning(self, "Error", "Failed to accept booking.")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def deny_booking(self):
        selected_item = self.booking_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "No booking selected.")
            return

        booking_id = selected_item.text().split(" ")[1]

        try:
            response = requests.post(
                f"http://localhost:8000/bookings/{booking_id}/deny",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Booking denied!")
                self.load_bookings()
            else:
                QMessageBox.warning(self, "Error", "Failed to deny booking.")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

import sys
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QListWidget, QMessageBox
import requests

class HotelCRUDWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()

        self.token = token
        self.setWindowTitle("Manage Hotels")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.hotel_list = QListWidget()
        layout.addWidget(self.hotel_list)

        self.refresh_button = QPushButton("Refresh Hotels")
        self.refresh_button.clicked.connect(self.load_hotels)
        layout.addWidget(self.refresh_button)

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_input)

        self.rooms_label = QLabel("Rooms:")
        self.rooms_input = QLineEdit()
        layout.addWidget(self.rooms_label)
        layout.addWidget(self.rooms_input)

        self.add_button = QPushButton("Add Hotel")
        self.add_button.clicked.connect(self.add_hotel)
        layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete Selected Hotel")
        self.delete_button.clicked.connect(self.delete_hotel)
        layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_hotels(self):
        try:
            response = requests.get("http://localhost:8000/hotels")
            if response.status_code == 200:
                hotels = response.json()
                self.hotel_list.clear()
                for hotel in hotels:
                    self.hotel_list.addItem(f"{hotel['name']} - {hotel['address']} ({hotel['rooms']} rooms)")
            else:
                QMessageBox.warning(self, "Error", "Failed to load hotels.")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def add_hotel(self):
        name = self.name_input.text()
        address = self.address_input.text()
        rooms = self.rooms_input.text()

        try:
            response = requests.post(
                "http://localhost:8000/hotels",
                json={"name": name, "address": address, "rooms": rooms},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Hotel added successfully!")
                self.load_hotels()
            else:
                QMessageBox.warning(self, "Error", "Failed to add hotel.")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def delete_hotel(self):
        selected_item = self.hotel_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "No hotel selected.")
            return

        hotel_name = selected_item.text().split(" - ")[0]

        try:
            response = requests.get("http://localhost:8000/hotels")
            if response.status_code == 200:
                hotels = response.json()
                hotel_id = next((hotel['hotel_id'] for hotel in hotels if hotel['name'] == hotel_name), None)
                if hotel_id:
                    delete_response = requests.delete(
                        f"http://localhost:8000/hotels/{hotel_id}",
                        headers={"Authorization": f"Bearer {self.token}"}
                    )
                    if delete_response.status_code == 200:
                        QMessageBox.information(self, "Success", "Hotel deleted successfully!")
                        self.load_hotels()
                    else:
                        QMessageBox.warning(self, "Error", "Failed to delete hotel.")
            else:
                QMessageBox.warning(self, "Error", "Failed to load hotels.")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

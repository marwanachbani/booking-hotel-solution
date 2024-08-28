import sys
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from hotel_crud import HotelCRUDWindow
from booking_management import BookingManagementWindow

class DashboardWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()

        self.token = token
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.hotel_button = QPushButton("Manage Hotels")
        self.hotel_button.clicked.connect(self.open_hotel_management)
        layout.addWidget(self.hotel_button)

        self.booking_button = QPushButton("Manage Bookings")
        self.booking_button.clicked.connect(self.open_booking_management)
        layout.addWidget(self.booking_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_hotel_management(self):
        self.hotel_management = HotelCRUDWindow(self.token)
        self.hotel_management.show()

    def open_booking_management(self):
        self.booking_management = BookingManagementWindow(self.token)
        self.booking_management.show()

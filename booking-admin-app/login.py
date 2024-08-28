import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
import requests

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Login")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        try:
            response = requests.post("http://localhost:8000/users/login", data={"email": email, "password": password})
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                self.role = data.get("role", "user")
                QMessageBox.information(self, "Login Successful", "Welcome to the Admin Dashboard!")
                self.open_dashboard()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid email or password.")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def open_dashboard(self):
        if self.role == "admin":
            from dashboard import DashboardWindow
            self.dashboard = DashboardWindow(self.token)
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(self, "Access Denied", "You are not authorized to access the admin dashboard.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

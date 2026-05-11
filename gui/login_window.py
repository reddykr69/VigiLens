import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("VigiLens - Login")
        self.setFixedSize(400, 450)
        self.setStyleSheet("background-color: #0F172A;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("VigiLens")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setStyleSheet("color: #4DB5E6;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("AI Surveillance System")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: #94A3B8;")
        subtitle.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: #1E293B;
                color: white;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 0 10px;
                font-size: 14px;
            }
        """)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(45)
        self.password_input.setStyleSheet(
            self.username_input.styleSheet()
        )

        self.login_button = QPushButton("Login")
        self.login_button.setFixedHeight(45)
        self.login_button.setStyleSheet("""
            QPushButton {
                background: #2563EB;
                color: white;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #1D4ED8;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)

        security_note = QLabel("Authorized Personnel Only")
        security_note.setStyleSheet(
            "color: #F59E0B; font-size: 11px;"
        )
        security_note.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(security_note)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "vigil123":
            self.close()
            self.on_login_success()
        else:
            QMessageBox.warning(
                self, "Login Failed",
                "Incorrect username or password."
            )
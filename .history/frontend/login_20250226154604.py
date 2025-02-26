import sys
import os
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QFrame, QCheckBox, QHBoxLayout
)
from PySide6.QtGui import QPixmap, QMovie, QFont, QImage, QPainter, QBrush
from PySide6.QtCore import Qt
from django.contrib.auth.hashers import check_password

# ✅ Get the Absolute Path of the Project
BASE_DIR = os.path.dirname(os.path.abspath("SMART"))

# ✅ Function to Apply Blur Effect to Background Image
def apply_blur(image_path):
    img = QImage(image_path)
    painter = QPainter(img)
    painter.setOpacity(0.5)  # Adjust blur opacity (0 = transparent, 1 = solid)
    painter.setBrush(QBrush(Qt.black))
    painter.drawRect(0, 0, img.width(), img.height())
    painter.end()
    return img

# ✅ Database Connection Function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bhup@2003",  # Replace with your actual MySQL password
        database="srm_db"
    )

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # ✅ Set Bigger Window Size
        self.setWindowTitle("Smart Relationship Management System - Login")
        self.setGeometry(200, 100, 1000, 562)  # Increased size

        # ✅ Set Background Image with Blur Effect
        self.bg_label = QLabel(self)
        bg_path = os.path.join(BASE_DIR, "background_login.png")  # Use absolute path

        if os.path.exists(bg_path):
            blurred_image = apply_blur(bg_path)  # Apply blur function
            self.bg_label.setPixmap(QPixmap.fromImage(blurred_image))
        else:
            print(f"⚠️ Warning: background_login.png not found at {bg_path}")

        self.bg_label.setGeometry(0, 0, 1000, 562)

        # ✅ Animated Logo (Optional)
        self.logo_label = QLabel(self)
        logo_path = os.path.join(BASE_DIR, "logo.gif")  # Use absolute path
        if os.path.exists(logo_path):
            movie = QMovie(logo_path)
            self.logo_label.setMovie(movie)
            self.logo_label.setAlignment(Qt.AlignCenter)
            movie.start()
        else:
            print(f"⚠️ Warning: logo.gif not found at {logo_path}")
            self.logo_label.setText("SRM")
            self.logo_label.setFont(QFont("Arial", 22, QFont.Bold))
            self.logo_label.setAlignment(Qt.AlignCenter)
            self.logo_label.setStyleSheet("color: white;")

        # ✅ Centered Login Box
        box_width = 350
        box_height = 370  # Increased height for new elements
        box_x = (1000 - box_width) // 2  # Center horizontally
        box_y = (562 - box_height) // 2  # Center vertically

        self.login_box = QFrame(self)
        self.login_box.setGeometry(box_x, box_y, box_width, box_height)
        self.login_box.setStyleSheet("background: rgba(255, 255, 255, 0.85); border-radius: 15px;")

        # ✅ Title (No Border, Clean Look)
        self.title = QLabel("Login", self)
        self.title.setFont(QFont("Arial", 22, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #333;")  # Dark text

        # ✅ Username Input (More Stylish)
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Enter Username")
        self.username.setFont(QFont("Arial", 12))
        self.username.setFixedWidth(250)
        self.username.setStyleSheet("""
            QLineEdit {
                background: white;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 10px;
                font-size: 14px;
            }
        """)

        # ✅ Password Input
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFont(QFont("Arial", 12))
        self.password.setFixedWidth(250)
        self.password.setStyleSheet("""
            QLineEdit {
                background: white;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 10px;
                font-size: 14px;
            }
        """)

        # ✅ Show Password Checkbox (Inside White Box)
        self.show_password = QCheckBox("Show Password", self)
        self.show_password.setStyleSheet("""
            QCheckBox {
                background: white;
                color: black;
                font-size: 12px;
                padding: 3px;
                border-radius: 5px;
            }
        """)
        self.show_password.stateChanged.connect(self.toggle_password_visibility)

        # ✅ Login Button (Stylish Hover Effect)
        self.login_button = QPushButton("Login", self)
        self.login_button.setFont(QFont("Arial", 12))
        self.login_button.setFixedWidth(250)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0053a6;
                border: 2px solid white;
            }
        """)
        self.login_button.clicked.connect(self.authenticate)

        # ✅ Forgot Password Button (Inside White Box)
        self.forgot_password_button = QPushButton("Forgot Password?", self)
        self.forgot_password_button.setStyleSheet("""
            QPushButton {
                background: white;
                color: black;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.forgot_password_button.clicked.connect(self.reset_password)

        # ✅ Layout for Centered Box
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.title, alignment=Qt.AlignCenter)
        layout.addWidget(self.username, alignment=Qt.AlignCenter)
        layout.addWidget(self.password, alignment=Qt.AlignCenter)
        layout.addWidget(self.show_password, alignment=Qt.AlignCenter)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.forgot_password_button, alignment=Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)

        # ✅ Set Layout Inside Login Box
        self.login_box.setLayout(layout)

    def toggle_password_visibility(self):
        """ Show/Hide password when checkbox is clicked """
        if self.show_password.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def reset_password(self):
        """ Forgot Password Popup """
        QMessageBox.information(self, "Reset Password", "Please contact admin to reset your password.")

    def authenticate(self):
        username = self.username.text()
        password = self.password.text()

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM core_user WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                hashed_password = result[0]
                if check_password(password, hashed_password):
                    QMessageBox.information(self, "Login Success", "Welcome to the SRM System!")
                else:
                    QMessageBox.warning(self, "Error", "Invalid Credentials!")
            else:
                QMessageBox.warning(self, "Error", "User not found!")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

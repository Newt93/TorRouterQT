import stem.process
import requests
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.label_ip = QLabel("Current IP:", self)
        self.label_ip.move(20, 20)
        self.ip_edit = QLineEdit(self)
        self.ip_edit.move(100, 20)
        self.ip_edit.setFixedWidth(200)
        self.ip_edit.setEnabled(False)

        self.route_button = QPushButton("Route Traffic", self)
        self.route_button.move(20, 60)
        self.route_button.clicked.connect(self.route_traffic)

        self.setWindowTitle("Traffic Router")
        self.setGeometry(100, 100, 340, 120)
        self.show()

    def route_traffic(self):
        # Start a Tor process to route traffic through
        with stem.process.launch_tor_with_config(
            config = {
                'SocksPort': str(9050),
                'ControlPort': str(9051),
            },
        ) as tor_process:
            # Set the HTTP proxy to route traffic through the Tor network
            proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050',
            }

            # Send a request to a website to retrieve the current IP address
            response = requests.get('http://checkip.amazonaws.com', proxies=proxies)
            current_ip = response.text.strip()

            # Update the IP address displayed in the GUI
            self.ip_edit.setText(current_ip)

app = QApplication([])
window = Window()
app.exec_()

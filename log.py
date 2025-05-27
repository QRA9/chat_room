import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QWidget
from PyQt6 import uic
from room import talk

class login(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("./login.ui", self)
        self.name = self.findChild(QLineEdit, 'log_name')
        self.conn = self.findChild(QPushButton, 'login')
        self.conn.clicked.connect(self.jump)

    def jump(self):
        self.tt = talk(name=self.name.text())
        self.tt.show()
        self.close()




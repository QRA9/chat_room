import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QWidget
from log import login


if __name__ == '__main__':
    app = QApplication(sys.argv)
    log = login()
    log.show()
    sys.exit(app.exec())

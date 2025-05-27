import time
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QWidget, QTextEdit
from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSignal
import socket

class recv_Thread(QThread):
    finished = pyqtSignal(str)
    def __init__(self, tcpc):
        super().__init__()
        self.tcpc = tcpc
    def run(self):
        while True:
            try:
                data = self.tcpc.recv(1024)
                if data:
                    self.finished.emit(data.decode('utf-8'))
                else:
                    break
            except Exception as e:
                print(f"data_error")
                break

class talk(QWidget):
    def __init__(self, name):
        super().__init__()
        uic.loadUi("./talk.ui", self)
        self.send = self.findChild(QPushButton, 'send')
        self.message = self.findChild(QTextEdit, 'message')
        self.all = self.findChild(QTextEdit, 'all')
        self.send.clicked.connect(self.send_mes)
        self.name = name
        self.tcpc = None
        self.recv_th = None
        self.sock_conn()

    def sock_conn(self):
        server_ip = '192.168.31.65'
        server_port = 2024
        try:
            self.tcpc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcpc.connect((server_ip, server_port))
            client_id = self.name
            self.tcpc.send(client_id.encode('utf-8'))
            print("send_name")
        except Exception as e:
            print(f"error {e}")
        self.recv_th = recv_Thread(self.tcpc)
        self.recv_th.finished.connect(self.update_ui)
        self.recv_th.start()

    def update_ui(self, data):
        self.all.append(data)

    def send_mes(self):
        if not self.tcpc:
            print("没有连接服务器")
            return
        try:
            message = self.message.toPlainText()
            if message:
                self.tcpc.send(message.encode('utf-8'))
                time.sleep(0.05)
            else:
                print("empty")
        except ConnectionAbortedError:
            print("连接被中止")
            return -1
        except ConnectionResetError:
            print("连接被重置")
            return -1
        except Exception as e:
            print(f"发送数据时发生异常: {e}")
            return -1

    def closeEvent(self, event):
        if self.recv_th:
            self.recv_th.stop()
            self.recv_th.wait()
        if self.tcpc:
            self.tcpc.close()
        event.accept()







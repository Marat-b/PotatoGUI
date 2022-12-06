import socket
import sys

from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QPushButton

from db.services.option_service import OptionService


class ChecklinkWindow(QDialog):
    def __init__(self, parent=None):
        super(ChecklinkWindow, self).__init__(parent)
        self.setWindowTitle('Проверка связи с сервером')
        self.initWindow()
        self.switched = False

    def initWindow(self):
        ipaddress = OptionService.get_option('server_ipaddress')
        port = OptionService.get_option('server_port')
        # print(f'ipaddress={ipaddress.Value}')
        if ipaddress is not None or port is not None:
            response = self.ping_server(ipaddress.Value, int(port.Value))
        else:
            response = False

        layout = QGridLayout(self)

        l = QLabel()
        if response:
            l.setText('<font color="green">Связь с сервером АИС ССОРП установлена</font>')
        else:
            l.setText('<font color="red">Связь с сервером АИС ССОРП не установлена</font>')
        layout.addWidget(l, 0, 0)

        self.btn_ok = QPushButton('Ok')
        layout.addWidget(self.btn_ok, 3, 0)
        self.btn_ok.clicked.connect(self.onClose)

    def ping_server(self, server: str, port: int, timeout=3):
        """ping server"""
        try:
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server, port))
        except OSError as error:
            return False
        else:
            s.close()
            return True

    def onClose(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ChecklinkWindow()
    win.show()
    sys.exit(app.exec())


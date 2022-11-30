import sys

from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton

from gui.login_window import LoginWindow


class DeviceWindow(QDialog):
    def __init__(self,  parent=None):
        super(DeviceWindow, self).__init__(parent)
        self.setWindowTitle('Конвейер')
        self.initWindow()
        self.switched = False

    def initWindow(self):
        layout = QGridLayout(self)
        layout.addWidget(QLabel('IP адрес'), 0, 0)
        self.ipaddress = QLineEdit(self, placeholderText='0.0.0.0')
        layout.addWidget(self.ipaddress, 0, 1)
        layout.addWidget(QLabel('Порт'), 1, 0)
        self.port = QLineEdit(self )
        layout.addWidget(self.port, 1, 1)
        layout.addWidget(QLabel('Вкл/Выкл'), 2, 0)

        self.btn_device = QPushButton('Выключено')
        self.btn_device.setCheckable(True)
        self.btn_device.setToolTip('Включение/Выключение устройства')
        layout.addWidget(self.btn_device, 2, 1)
        self.btn_device.clicked.connect(self.onSwitch)

        self.btn_ok = QPushButton('Сохранить')
        layout.addWidget(self.btn_ok, 3, 0)
        self.btn_ok.clicked.connect(self.onClose)

        self.btn_cancel = QPushButton('Отменить')
        layout.addWidget(self.btn_cancel, 3, 1)
        self.btn_cancel.clicked.connect(self.onClose)

    def onClose(self):
        self.close()

    def onSwitch(self):
        self.switched = False if self.switched else True
        if self.switched:
            self.btn_device.setText('Включено')
        else:
            self.btn_device.setText('Выключено')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DeviceWindow()
    win.show()
    sys.exit(app.exec())
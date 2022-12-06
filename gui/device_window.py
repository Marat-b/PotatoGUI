import sys

from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton

from db.services.option_service import OptionService


class DeviceWindow(QDialog):
    def __init__(self,  parent=None):
        super(DeviceWindow, self).__init__(parent)
        self.setWindowTitle('Конвейер')
        self.initWindow()
        self.switched = False

    def initWindow(self):
        layout = QGridLayout(self)
        layout.addWidget(QLabel('IP адрес'), 0, 0)
        ipaddress = OptionService.get_option('device_ipaddress')
        if ipaddress is not None:
            self.ipaddress = QLineEdit(ipaddress.Value)
        else:
            self.ipaddress = QLineEdit(self, placeholderText='0.0.0.0')
        layout.addWidget(self.ipaddress, 0, 1)

        print('++++++++++++++++++')
        port = OptionService.get_option('device_port')
        layout.addWidget(QLabel('Порт'), 1, 0)
        if port is not None:
            self.port = QLineEdit(port.Value)
        else:
            self.port = QLineEdit(self )
        layout.addWidget(self.port, 1, 1)
        layout.addWidget(QLabel('Вкл/Выкл'), 2, 0)

        self.btn_device = QPushButton('Выключено')
        self.btn_device.setCheckable(True)
        self.btn_device.setToolTip('Включение/Выключение устройства')
        layout.addWidget(self.btn_device, 2, 1)
        self.btn_device.clicked.connect(self.onSwitch)
        switched = OptionService.get_option('device_context')
        if switched is not None:
            self.switched = True if switched.Value == '1' else False
            if self.switched:
                self.btn_device.setText('Включено')
            else:
                self.btn_device.setText('Выключено')


        self.btn_ok = QPushButton('Сохранить')
        layout.addWidget(self.btn_ok, 3, 0)
        self.btn_ok.clicked.connect(self.onSave)

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


    def onSave(self):
        OptionService.update_option('device_ipaddress', self.ipaddress.text())
        OptionService.update_option('device_port', self.port.text())
        OptionService.update_option('device_context', self.switched)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DeviceWindow()
    win.show()
    sys.exit(app.exec())
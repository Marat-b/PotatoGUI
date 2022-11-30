import sys

from PyQt5.QtWidgets import QApplication, QComboBox, QDesktopWidget, QDialog, QFormLayout, QGridLayout, QLabel, \
    QLineEdit, \
    QMainWindow, \
    QMessageBox, QPushButton, \
    QWidget

from classes.http_request import HttpRequest


class LoginWindow(QDialog):
    def __init__(self, data, parent=None):
        # super(LoginWindow, self).__init__()
        super(LoginWindow, self).__init__(parent)
        self.hr = HttpRequest()
        self._data = data
        # token = None
        # self.setLayout(QGridLayout())
        # cent = QDesktopWidget().availableGeometry().center()  # Finds the center of the screen
        # self.setStyleSheet("background-color: white;")
        # self.resize(1400, 800)
        # self.frameGeometry().moveCenter(cent)
        self.setWindowTitle('Potato Login')
        self.initWindow()
        # self.setCentralWidget(self.widget)
        # self.show()

    def initWindow(self):
        # set layout
        layout = QGridLayout(self)
        # self.widgetd = QWidget()
        # self.widgetd.setLayout(layout)

        layout.addWidget(QLabel('IP-адрес сервера'), 0, 0)

        self.widget_ipaddress = QLineEdit('erp.bk-nt.ru', self)
        layout.addWidget(self.widget_ipaddress, 1, 0)
        # self.widget_ipaddress.move(0, 1)

        layout.addWidget(QLabel('Порт сервера'), 2, 0)

        self.widget_ipport = QLineEdit('', self)
        layout.addWidget(self.widget_ipport, 3, 0)
        # self.widget_ipport.move(0, 1)

        layout.addWidget(QLabel('Ведите пинкод'), 4, 0)

        self.widget_pincode = QLineEdit('', self)
        layout.addWidget(self.widget_pincode, 5, 0)
        # self.widget_pincode.move(0, 1)

        self.widget_button_pincode = QPushButton('Ввод')
        layout.addWidget(self.widget_button_pincode, 5, 1)
        self.widget_button_pincode.clicked.connect(self.onPincode)

        layout.addWidget(QLabel('Выберите пользователя'), 6, 0)
        self.widget_users = QComboBox()
        layout.addWidget(self.widget_users, 7, 0)

        self.widget_button_users = QPushButton('Выбрать')
        layout.addWidget(self.widget_button_users, 7, 1)
        self.widget_button_users.clicked.connect(self.onChooseUser)
        self.widget_button_users.setEnabled(False)

    def onPincode(self):
        pincode = self.widget_pincode.text()
        token = self.hr.get_point(pincode)
        if token is not None:
            self.widget_button_users.setEnabled(True)
            self._data['token'] = token
            users = self.hr.get_check(self._data['token'])
            for user in users:
                print(f'user_id={user["id"]}')
                self.widget_users.addItem(f'{user["surname"]} {user["name"]} {user["patronymic"]}', user["id"] )
        else:
            # box = QMessageBox.warning(self, 'Внимание', 'Пинкод не верен или нет связи')
            box = QMessageBox()
            box.setIcon(QMessageBox.Warning)
            box.setText('Пинкод не верен или нет связи')
            box.setWindowTitle('Внимание')
            box.setStandardButtons(QMessageBox.Yes)
            buttonY = box.button(QMessageBox.Yes)
            buttonY.setText('Продолжить...')
            box.exec()
            self.accept()


    def onChooseUser(self):
        self.user_id = self.widget_users.currentIndex()
        print(f'self.widget_users.itemData={self.widget_users.itemData(self.widget_users.currentIndex())}')
        self._data['operator_id'] = self.widget_users.itemData(self.widget_users.currentIndex())
        self.fill_data()
        self.accept()


    def accept(self):
        super().accept()

    def fill_data(self):
        try:
            words = self.widget_users.currentText().split(' ')
            self._data['operator_name'] = words[0]
            self._data['operator_surname'] = words[1]
            self._data['operator_patronymic'] = words[2]
        except:
            pass

if __name__ == "__main__":
    token='Zero'
    app = QApplication(sys.argv)
    win = LoginWindow(token)
    win.show()
    print(f'win.token={token}')
    # win = MyWindow()
    # win.show()
    sys.exit(app.exec())
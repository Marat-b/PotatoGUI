import sys

from PyQt5.QtWidgets import QApplication, QComboBox, QDesktopWidget, QDialog, QFormLayout, QGridLayout, QLabel, \
    QLineEdit, \
    QMainWindow, \
    QMessageBox, QPushButton, \
    QWidget

from classes.http_request import HttpRequest
from db.app_database import create_db_and_tables
from db.services.option_service import OptionService
from db.services.parameter_service import ParameterService
from gui.password_window import PasswordWindow

SERVER_IPADDRESS = 'server_ipaddress'
SERVER_PORT = 'server_port'


class LoginWindow(QDialog):
    def __init__(self, data, parent=None):
        # super(LoginWindow, self).__init__()
        super(LoginWindow, self).__init__(parent)
        self._data = data
        self.ip_address = OptionService.get_option(SERVER_IPADDRESS)
        self.ip_port = OptionService.get_option(SERVER_PORT)
        self.users = None
        if self.ip_address is not None:
            self.hr = HttpRequest(ip_address=self.ip_address.Value, port=self.ip_port.Value)
            self._data['ip_address'] = self.ip_address.Value
            self._data['port'] = self.ip_port.Value
        else:
            self.hr = HttpRequest()


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

        if self.ip_address is None:
            self.widget_ipaddress = QLineEdit('', self)  # erp.bk-nt.ru
        else:
            self.widget_ipaddress = QLineEdit(self.ip_address.Value, self)
        layout.addWidget(self.widget_ipaddress, 1, 0)
        # self.widget_ipaddress.move(0, 1)

        layout.addWidget(QLabel('Порт сервера'), 2, 0)
        if self.ip_port is None:
            self.widget_ipport = QLineEdit('', self)
        else:
            self.widget_ipport = QLineEdit(self.ip_port.Value, self)
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

        ########## get token from DB ################
        token = OptionService.get_option('token')
        print(f'token -  {token}')
        if token is not None:
            self.widget_button_users.setEnabled(True)
            self._data['token'] = token.Value
            # OptionService.update_option('token', token)
            self.point_data = self.hr.get_check(self._data['token'])
            if self.point_data is not None:
                self.users = self.point_data["users"]
                self._data['current_client'] = self.point_data["configuration"]["client"]
                # self._data['nomenclatures'] = self.point_data["nomenclatures"]
                print(f'self.users={self.users}')
                if self.users is not None:
                    for i, user in enumerate(self.users):
                        print(f'user_id={user["id"]}')
                        self.widget_users.addItem(f'{user["surname"]} {user["name"]} {user["patronymic"]}', i)
                # save pararmeters to db
                ParameterService.save_cars(self.point_data["cars"])
                ParameterService.save_nomenclatures(self.point_data["nomenclatures"])
                ParameterService.save_providers(self.point_data["recipients"])

    def onPincode(self):
        self.hr(ip_address=self.widget_ipaddress.text(), port=self.widget_ipport.text())
        pincode = self.widget_pincode.text()
        token = self.hr.get_point(pincode)
        if token is not None:
            OptionService.update_option('token', token)
            self.save_data_to_db()
            self.widget_button_users.setEnabled(True)
            self._data['token'] = token
            self._data['ip_address'] = self.widget_ipaddress.text()
            self._data['port'] = self.widget_ipport.text()

            self.point_data = self.hr.get_check(self._data['token'])
            if self.point_data is not None:
                self.users = self.point_data["users"]
                self._data['current_client'] = self.point_data["configuration"]["client"]
                # self._data['nomenclatures'] = self.point_data["nomenclatures"]
                if len(self.users) > 0:
                    self.widget_users.clear()
                for i, user in enumerate(self.users):
                    print(f'user_id={user["id"]}')
                    self.widget_users.addItem(f'{user["surname"]} {user["name"]} {user["patronymic"]}', i)
                    # save pararmeters to db
                    ParameterService.save_cars(self.point_data["cars"])
                    ParameterService.save_nomenclatures(self.point_data["nomenclatures"])
                    ParameterService.save_providers(self.point_data["recipients"])
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
        # self.user_id = self.widget_users.currentIndex()
        current_index = self.widget_users.currentIndex()
        print(f'current_index={current_index}')
        print(f'self.users={self.users}')
        if self.users is not None:
            print(f'self.widget_users.itemData={self.widget_users.itemData(current_index)}')
            print(f"self.users[current_index]['phone']={self.users[current_index]['phone']}")
            self._data['operator_id'] = self.users[current_index]['id'] #self.widget_users.itemData(
            # self._data['current_client'] = self.users[current_index]['current_client']
            password = {'password': ''}
            pw = PasswordWindow(password)
            pw.exec()
            print(f'self.password={password}')
            ret = self.hr.check_password(self.users[current_index]['phone'], password['password'])
            # print(f'ret token={ret}')
            if ret is not None:
                print('password is true')
                self._data['password'] = '1'
                self._data['user_token'] = ret['token']
                dashboard_data = self.hr.get_check_dashboard(ret['token'], self._data['current_client'])
                if dashboard_data is not None:
                    self._data['user_token'] = dashboard_data['token']
                    ParameterService.save_recipient(dashboard_data['client']['legal']['name']['short'])
            else:
                print('password is false')
            self.fill_data()
            self.accept()

    def accept(self):
        super().accept()

    def fill_data(self):
        try:
            words = self.widget_users.currentText().split(' ')
            self._data['operator_name'] = words[1]
            self._data['operator_surname'] = words[0]
            self._data['operator_patronymic'] = words[2]

        except:
            pass

    def save_data_to_db(self):
        OptionService.update_option(SERVER_IPADDRESS, self.widget_ipaddress.text())
        OptionService.update_option(SERVER_PORT, self.widget_ipport.text())


if __name__ == "__main__":
    token = 'Zero'
    create_db_and_tables()
    app = QApplication(sys.argv)
    win = LoginWindow(token)
    win.show()
    print(f'win.token={token}')
    # win = MyWindow()
    # win.show()
    sys.exit(app.exec())

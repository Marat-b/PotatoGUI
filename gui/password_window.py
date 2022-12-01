import sys

from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton


class PasswordWindow(QDialog):
    def __init__(self, data, parent=None):
        super(PasswordWindow, self).__init__(parent)
        self.setWindowTitle('Ввод пароля')
        self.initWindow()
        self.switched = False
        self._data = data

    def initWindow(self):
        layout = QGridLayout(self)
        layout.addWidget(QLabel('Введите пароль'), 0, 0)
        self.widget_password = QLineEdit('', self)
        self.widget_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.widget_password, 1, 0)

        self.btn_ok = QPushButton('Ok')
        layout.addWidget(self.btn_ok, 2, 0)
        self.btn_ok.clicked.connect(self.onClose)

    def onClose(self):
        self.close()
        self._data['password'] = self.widget_password.text()
        self.accept()

    def accept(self):
        super().accept()

if __name__ == '__main__':
    # password = {}
    password = {'password': ''}
    app = QApplication(sys.argv)
    win = PasswordWindow(password)
    win.show()
    print(f'password={password}')
    sys.exit(app.exec())

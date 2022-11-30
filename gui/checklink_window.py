import sys

from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QPushButton


class ChecklinkWindow(QDialog):
    def __init__(self, parent=None):
        super(ChecklinkWindow, self).__init__(parent)
        self.setWindowTitle('Проверка связи с сервером')
        self.initWindow()
        self.switched = False

    def initWindow(self):
        layout = QGridLayout(self)

        l = QLabel()
        l.setText('<font color="green">Связь с сервером АИС ССОРП установлена</font>')
        layout.addWidget(l, 0, 0)

        self.btn_ok = QPushButton('Ok')
        layout.addWidget(self.btn_ok, 3, 0)
        self.btn_ok.clicked.connect(self.onClose)

    def onClose(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ChecklinkWindow()
    win.show()
    sys.exit(app.exec())


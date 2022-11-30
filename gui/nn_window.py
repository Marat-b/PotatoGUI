import sys

from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QPushButton, QSpinBox


class NnWindow(QDialog):
    def __init__(self,  parent=None):
        super(NnWindow, self).__init__(parent)
        self.setWindowTitle('Нейронная сеть')
        self.initWindow()
        self.switched = False

    def initWindow(self):
        layout = QGridLayout(self)
        layout.addWidget(QLabel('Точность распознования объекта,%'), 0, 0)
        accuracy = QSpinBox(value=50, maximum=100, minimum=10, singleStep=10)
        layout.addWidget(accuracy, 0, 1)

        self.btn_ok = QPushButton('Сохранить')
        layout.addWidget(self.btn_ok, 3, 0)
        self.btn_ok.clicked.connect(self.onClose)

        self.btn_cancel = QPushButton('Отменить')
        layout.addWidget(self.btn_cancel, 3, 1)
        self.btn_cancel.clicked.connect(self.onClose)

    def onClose(self):
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = NnWindow()
    win.show()
    sys.exit(app.exec())


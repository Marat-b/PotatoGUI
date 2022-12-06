import sys

from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QGridLayout, QLabel, QPushButton, QSpinBox

from db.services.option_service import OptionService


class NnWindow(QDialog):
    def __init__(self,  parent=None):
        super(NnWindow, self).__init__(parent)
        self.setWindowTitle('Нейронная сеть')
        self.initWindow()
        self.switched = False

    def initWindow(self):
        self.nn_accuracy = OptionService.get_option('nn_accuracy')
        self.nn_configuration = OptionService.get_option('nn_configuration')
        layout = QGridLayout(self)

        layout.addWidget(QLabel('Точность распознования объекта,%'), 0, 0)

        if self.nn_accuracy is not None:
            self.accuracy_widget = QSpinBox(value=int(self.nn_accuracy.Value), maximum=100, minimum=10, singleStep=10)
        else:
            self.accuracy_widget = QSpinBox(value=50, maximum=100, minimum=10, singleStep=10)
        layout.addWidget(self.accuracy_widget, 0, 1)

        layout.addWidget(QLabel('Конфигурация нейронной сети'), 1, 0)

        self.configuration_widget = QComboBox()
        self.configuration_widget.addItem('Конфигурация 1 от 22.09.22', 0)
        self.configuration_widget.addItem('Конфигурация 2 от 23.10.22', 1)
        self.configuration_widget.addItem('Конфигурация 3 от 30.10.22', 2)
        self.configuration_widget.addItem('Конфигурация 4 от 02.11.22', 3)
        self.configuration_widget.addItem('Конфигурация 5 от 15.11.22', 4)
        self.configuration_widget.addItem('Конфигурация 6 от 29.11.22', 5)
        layout.addWidget(self.configuration_widget, 1, 1)
        if self.nn_configuration is not None:
            index = int(self.nn_configuration.Value)
            self.configuration_widget.setCurrentIndex(index)

        self.btn_ok = QPushButton('Сохранить')
        layout.addWidget(self.btn_ok, 3, 0)
        self.btn_ok.clicked.connect(self.onSave)

        self.btn_cancel = QPushButton('Отменить')
        layout.addWidget(self.btn_cancel, 3, 1)
        self.btn_cancel.clicked.connect(self.onClose)

    def onClose(self):
        self.close()

    def onSave(self):
        OptionService.update_option('nn_accuracy', self.accuracy_widget.value())
        OptionService.update_option('nn_configuration', self.configuration_widget.currentIndex())
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = NnWindow()
    win.show()
    sys.exit(app.exec())


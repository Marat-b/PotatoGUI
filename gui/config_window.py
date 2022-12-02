import sys

from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit

from db.services.option_service import OptionService


class ConfigWindow(QDialog):
    def __init__(self, parent=None):
        super(ConfigWindow, self).__init__(parent)
        self.setWindowTitle('Конфигурация')
        self.initWindow()
        self.switched = False

    def initWindow(self):
        detectron2 = ''
        # detectron2 = OptionService.get_option('detectron2')
        # deepsort = OptionService.get_option('deepsort')
        # display_width = OptionService.get_option('display_width')
        # display_height = OptionService.get_option('display_height')
        # max_dist = OptionService.get_option('max_dist')
        # num_classes = OptionService.get_option('num_classes')
        # use_cuda = OptionService.get_option('use_cuda')
        # video_path = OptionService.get_option('video_path')

        layout = QGridLayout(self)

        layout.addWidget(QLabel('Путь к файлу detectron2'), 0, 0)

        if detectron2 is not None:
            self.widget_detectron2 = QLineEdit(detectron2)
        else:
            self.widget_detectron2 = QLineEdit(self, placeholder='Путь к файлу detectron2')
        layout.addWidget(self.widget_detectron2, 0, 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ConfigWindow()
    win.show()
    sys.exit(app.exec())
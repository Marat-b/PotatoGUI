import sys

from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, \
    QSpinBox

from db.services.config_service import ConfigService
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

        # layout.addWidget(QLabel('Путь к файлу detectron2'), 0, 0)
        #
        # if detectron2 is not None:
        #     self.widget_detectron2 = QLineEdit(detectron2)
        # else:
        #     self.widget_detectron2 = QLineEdit(self, placeholder='Путь к файлу detectron2')
        # layout.addWidget(self.widget_detectron2, 0, 1)

        video_group = QGroupBox('Видео')
        video_group.setLayout(QGridLayout())
        video_group.layout().addWidget(QLabel('Ширина'), 0, 0)
        self.video_width = QSpinBox(self, value=ConfigService.get_video_width(), maximum=2000, minimum=100,
                                    singleStep=10)
        self.video_width.setValue(ConfigService.get_video_width())
        video_group.layout().addWidget(self.video_width, 0, 1)

        video_group.layout().addWidget(QLabel('Высота'), 1, 0)
        self.video_height = QSpinBox(value=ConfigService.get_video_height(), maximum=2000, minimum=200, singleStep=10)
        self.video_height.setValue(ConfigService.get_video_height())
        video_group.layout().addWidget(self.video_height, 1, 1)


        video_group.layout().addWidget(QLabel('Путь хранения видеофайлов'), 2, 0)
        self.video_path = QLineEdit(ConfigService.get_video_path(), self)
        video_group.layout().addWidget(self.video_path, 2, 1)

        btn_video_path = QPushButton('...')
        video_group.layout().addWidget(btn_video_path, 2, 2)
        btn_video_path.clicked.connect(self.onChoosePath)

        layout.addWidget(video_group, 1, 0, 1, 2)

        btn_group = QGroupBox('')
        btn_group.setLayout(QHBoxLayout())
        # btn_group.setStyleSheet('border: none')
        btn_ok = QPushButton('Сохранить')
        btn_group.layout().addWidget(btn_ok)
        btn_ok.clicked.connect(self.onSave)

        btn_cancel = QPushButton('Отменить')
        btn_group.layout().addWidget(btn_cancel)
        btn_cancel.clicked.connect(self.onCancel)


        layout.addWidget(btn_group, 2, 0, 1, 2)

    def onCancel(self):
        self.close()

    def onChoosePath(self):
        path = QFileDialog.getExistingDirectory(self, 'Выбери каталог')
        print(f'path={path}')
        self.video_path.setText(path)

    def onSave(self):
        ConfigService.save_video_height(self.video_height.text())
        ConfigService.save_video_path(self.video_path.text())
        ConfigService.save_video_width(self.video_width.text())
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ConfigWindow()
    win.show()
    sys.exit(app.exec())
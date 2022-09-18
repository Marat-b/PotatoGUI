from PyQt5 import QtCore, QtGui
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QComboBox, QDesktopWidget, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QMainWindow, \
    QMessageBox, QPushButton, \
    QSpinBox, QStatusBar, \
    QWidget, \
    QApplication, \
    QLabel, \
    QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

from classes.http_request import HttpRequest
from classes.video_thread import VideoThread


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.hr = HttpRequest()
        self.widget_botanical_variety = None
        self.class_names_ru = ['здоровая', 'альтернириоз', 'антракноз', 'фомоз (пуговичная гниль)',
                               'фузариоз (сухая гниль)', 'внутренняя гниль',
                               'некроз', 'фитофтороз', 'розовая гниль', 'парша', 'мокрая гниль']
        self.classes = {}
        self.sizes = {'big': 0, 'middle': 0, 'small': 0, 'result': 0}
        self.available_cameras = QCameraInfo.availableCameras()  # Getting available cameras

        cent = QDesktopWidget().availableGeometry().center()  # Finds the center of the screen
        # self.setStyleSheet("background-color: white;")
        # self.resize(1400, 800)
        self.frameGeometry().moveCenter(cent)
        self.setWindowTitle('Potato MVP')
        self.initWindow()

        self.setCentralWidget(self.widget)
        self.show()

    ########################################################################################################################
    #                                                   Windows                                                            #
    ########################################################################################################################
    def initWindow(self):
        # create the video capture thread
        self.thread = VideoThread()
        # set layout
        self.layout = QGridLayout(self)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        # Button to start video
        self.ss_video = QPushButton(self)
        self.ss_video.setText('Начать')
        self.layout.addWidget(self.ss_video, 7, 8)
        self.ss_video.clicked.connect(self.ClickStartVideo)

        self.btn_http = QPushButton('http save')
        self.layout.addWidget(self.btn_http, 7, 9)
        self.btn_http.clicked.connect(self.onRequest)

        self.btn_clear = QPushButton('Очистить')
        self.layout.addWidget(self.btn_clear, 7, 10)
        self.btn_clear.clicked.connect(self.onClear)

        # Quit button
        self.btn_quit = QPushButton(self)
        self.btn_quit.setText('Выход')
        self.layout.addWidget(self.btn_quit, 7, 11)
        self.btn_quit.clicked.connect(self.onClose)

        # Video
        self.image_label = QLabel(self)
        self.disply_width = 640
        self.display_height = 480
        self.image_label.setStyleSheet("background : black;")
        self.layout.addWidget(self.image_label, 0, 0, 8, 8)

        self.layout.addWidget(QLabel('Р Е З У Л Ь Т А Т Ы'), 9, 2, 1, 3)

        groupbox_size = QGroupBox('Размеры')
        groupbox_size.setLayout(QGridLayout())
        self.layout.addWidget(groupbox_size, 10, 0, 1, 4)

        groupbox_size.layout().addWidget(QLabel('Общее количество'), 0, 0, 1, 3)
        self.result = QLabel('0')
        groupbox_size.layout().addWidget(self.result, 0, 4)
        groupbox_size.layout().addWidget(QLabel('Крупный размер'), 1, 0, 1, 3)
        self.big_size = QLabel('0')
        groupbox_size.layout().addWidget(self.big_size, 1, 4)
        groupbox_size.layout().addWidget(QLabel('Средний размер'), 2, 0, 1, 3)
        self.middle_size = QLabel('0')
        groupbox_size.layout().addWidget(self.middle_size, 2, 4)
        groupbox_size.layout().addWidget(QLabel('Мелкий размер'), 3, 0, 1, 3)
        self.small_size = QLabel('0')
        groupbox_size.layout().addWidget(self.small_size, 3, 4)

        x = 0
        groupbox_sick = QGroupBox('Болезни')
        groupbox_sick.setLayout(QGridLayout())
        self.layout.addWidget(groupbox_sick, 10, 5, 1, 4)
        self.class_widgets = {}
        for i, class_name in enumerate(self.class_names_ru):
            groupbox_sick.layout().addWidget(QLabel(class_name), x + i, 0, 1, 3)
            self.class_widgets[i] = QLabel('0')
            groupbox_sick.layout().addWidget(self.class_widgets[i], x + i, 4)

        # ----------------------------------------------------------------
        groupbox = QGroupBox('Параметры')
        groupbox.setLayout(QGridLayout())
        self.layout.addWidget(groupbox, 0, 8, 1, 4)

        groupbox.layout().addWidget(QLabel('Сорт картофеля'), 0, 0)
        self.widget_botanical_variety = QComboBox()
        self.widget_botanical_variety.addItem('Аспия', 0)
        self.widget_botanical_variety.addItem('Белорусская', 1)
        groupbox.layout().addWidget(self.widget_botanical_variety, 0, 1)

        groupbox.layout().addWidget(QLabel('Заявленный объём'), 1, 0)
        self.widget_declared_volume = QSpinBox(value=1, maximum=100, minimum=1, singleStep=1)
        groupbox.layout().addWidget(self.widget_declared_volume, 1, 1)

        groupbox.layout().addWidget(QLabel('Транспортное средство'), 2, 0)
        self.widget_truck = QComboBox()
        self.widget_truck.addItem('КАМАЗ', 0)
        self.widget_truck.addItem('Газель', 1)
        groupbox.layout().addWidget(self.widget_truck, 2, 1)

        groupbox.layout().addWidget(QLabel('Поставщик'), 3, 0)
        self.widget_provider = QComboBox()
        self.widget_provider.addItem('ООО Ромашка', 0)
        self.widget_provider.addItem('ООО Промокашка', 1)
        groupbox.layout().addWidget(self.widget_provider, 3, 1)

        groupbox.layout().addWidget(QLabel('Направление'), 4, 0)
        self.widget_direction = QComboBox()
        self.widget_direction.addItem('Приёмка', 0)
        self.widget_direction.addItem('Отъёмка', 1)
        groupbox.layout().addWidget(self.widget_direction, 4, 1)

        # Status bar
        self.status = QStatusBar()
        self.status.setStyleSheet("background : lightblue;")  # Setting style sheet to the status bar
        self.setStatusBar(self.status)  # Adding status bar to the main window
        self.status.showMessage('Ready to start')

    ######################################################################
    #                                   Events                           #
    ######################################################################
    def onClose(self):
        self.thread.stop()
        self.close()

    def onClear(self):
        self.result.setText("0")
        self.big_size.setText("0")
        self.middle_size.setText("0")
        self.small_size.setText("0")

        self.hr.total_count("0")
        self.hr.large_caliber("0")
        self.hr.medium_caliber("0")
        self.hr.small_caliber("0")
        for i, class_name in enumerate(self.class_names_ru):
            self.class_widgets[i].setText("0")

        self.status.showMessage('Данные очищены')




    def onRequest(self):
        self.hr.send_request()
        QMessageBox.information(self, 'Информация', 'Данные отправлены на Веб сервер.')



    ############################################################################
    #                                    Buttons                               #
    ############################################################################
    # Activates when Start/Stop video button is clicked to Start (ss_video
    def ClickStartVideo(self):
        self.hr.start_date()
        self.hr.start_time()
        # Change label color to light blue
        self.ss_video.clicked.disconnect(self.ClickStartVideo)
        self.status.showMessage('Идёт трансляция...')
        # Change button to stop
        self.ss_video.setText('Пауза')
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)

        # start the thread
        self.thread.start()
        self.ss_video.clicked.connect(self.thread.stop)  # Stop the video if button clicked
        self.ss_video.clicked.connect(self.ClickStopVideo)

    # Activates when Start/Stop video button is clicked to Stop (ss_video)
    def ClickStopVideo(self):
        self.thread.change_pixmap_signal.disconnect()
        self.ss_video.setText('Начать')
        self.status.showMessage('Трансляция остановлена')
        self.ss_video.clicked.disconnect(self.ClickStopVideo)
        self.ss_video.clicked.disconnect(self.thread.stop)
        self.ss_video.clicked.connect(self.ClickStartVideo)
        ######## update data #########################
        self.hr.botanical_variety(self.widget_botanical_variety.currentText())
        self.hr.declared_volume(str(self.widget_declared_volume.value()))
        self.hr.car(self.widget_truck.currentText())
        self.hr.provider(self.widget_provider.currentText())
        # self.hr.direction = self.widget_direction.currentText()
        self.hr.total_count(str(self.sizes['result']))
        self.hr.large_caliber(str(self.sizes['big']))
        self.hr.medium_caliber(str(self.sizes['middle']))
        self.hr.small_caliber(str(self.sizes['small']))
        ######## classes ####################
        self.hr.phytophthora(self.class_widgets[7].text())
        self.hr.end_date()
        self.hr.end_time()
        self.status.showMessage('Трансляция остановлена, данные сохранены')

    ########################################################################################################################
    #                                                   Actions                                                            #
    ########################################################################################################################

    def update_classes(self, classes):
        for key in classes.keys():
            self.class_widgets[key].setText(str(classes[key]))

    def update_image(self, cv_img, item_sorted, class_sorted):
        """Updates the image_label with a new opencv image"""
        print(f'update_image class_sorted={class_sorted}')
        self.update_sizes(item_sorted)
        self.update_classes(class_sorted)
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def update_sizes(self, sizes):
        if len(sizes) > 0:
            if 'big' in sizes:
                self.sizes['big'] = sizes['big']
                self.big_size.setText(str(sizes['big']))
            if 'middle' in sizes:
                self.sizes['middle'] = sizes['middle']
                self.middle_size.setText(str(sizes['middle']))
            if 'small' in sizes:
                self.sizes['small'] = sizes['small']
                self.small_size.setText(str(sizes['small']))
            self.sizes['result'] = self.sizes['big'] + self.sizes['middle'] + self.sizes['small']
            self.result.setText(str(self.sizes['result']))

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        # p = convert_to_Qt_format.scaled(801, 801, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    # win.show()
    sys.exit(app.exec())

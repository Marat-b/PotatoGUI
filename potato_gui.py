import datetime
import time

from PyQt5 import QtGui
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QAction, QCheckBox, QComboBox, QDesktopWidget, QGridLayout, QGroupBox, \
    QHBoxLayout, QLineEdit, QMainWindow, \
    QMessageBox, QPushButton, \
    QSpinBox, QStatusBar, \
    QWidget, \
    QApplication, \
    QLabel
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import Qt

from classes.http_request import HttpRequest
from classes.request_data import RequestData
from classes.video_thread_oak import VideoThread
from config.create_dirs import create_dirs
from db.app_database import create_db_and_tables
from db.save_session_data import save_session_data
from db.send_session_data import send_session_data
from db.services.parameter_service import ParameterService
from gui.checklink_window import ChecklinkWindow
from gui.device_window import DeviceWindow
from gui.login_window import LoginWindow
from gui.nn_window import NnWindow
from gui.print_window import PrintWindow


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.hr = HttpRequest()
        self.rd = RequestData()
        # self.widget_botanical_variety = None
        # self.class_names_ru = ['здоровая', 'альтернириоз', 'антракноз', 'фомоз (пуговичная гниль)',
        #                        'фузариоз (сухая гниль)', 'внутренняя гниль',
        #                        'некроз', 'фитофтороз', 'розовая гниль', 'парша', 'мокрая гниль']
        self.class_names_ru = ['здоровая', 'гнилая']

        self.classes = {}
        self.sizes = {'big': 0, 'middle': 0, 'small': 0, 'result': 0}
        self.obj = {
            'token': None, 'operator_id': '', 'operator_name': '', 'operator_surname': '',
            'operator_patronymic': '', 'ip_address': '', 'port': '', 'password': '0', 'user_token': '',
             'current_client': ''
        }
        self.available_cameras = QCameraInfo.availableCameras()  # Getting available cameras
        self.save_video = False
        self.thread = VideoThread()

        cent = QDesktopWidget().availableGeometry().center()  # Finds the center of the screen
        # self.setStyleSheet("background-color: white;")
        # self.resize(1400, 800)
        self.frameGeometry().moveCenter(cent)
        self.setWindowTitle('АРМ Оператора ССОРП')
        self.initWindow()
        self.initMenu()

        self.setCentralWidget(self.widget)
        self.show()

    ########################################################################################################################
    #                                                   Windows                                                            #
    ########################################################################################################################
    def initWindow(self):
        lw = LoginWindow(self.obj)
        lw.exec()
        # self.rd.operator_id = self.obj['operator_id']
        self.fill_from_data()
        print(f'self.obj={self.obj}')
        # create the video capture thread
        self.thread = VideoThread()
        # set layout
        self.layout = QGridLayout(self)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        ############################## Button to start video ##################
        group_button = QGroupBox()
        group_button.setLayout(QHBoxLayout())
        self.layout.addWidget(group_button, 7, 8)

        self.ss_video = QPushButton(self)
        self.ss_video.setText('Начать')
        group_button.layout().addWidget(self.ss_video)
        self.ss_video.clicked.connect(self.ClickStartVideo)

        self.btn_http = QPushButton('Отправить')
        group_button.layout().addWidget(self.btn_http)
        self.btn_http.clicked.connect(self.onRequest)
        self.btn_http.setEnabled(False)

        self.btn_print = QPushButton('Печать')
        group_button.layout().addWidget(self.btn_print)
        self.btn_print.clicked.connect(self.onPrint)

        self.btn_clear = QPushButton('Очистить')
        group_button.layout().addWidget(self.btn_clear)
        self.btn_clear.clicked.connect(self.onClear)

        # Quit button
        self.btn_quit = QPushButton(self)
        self.btn_quit.setText('Выход')
        group_button.layout().addWidget(self.btn_quit)
        self.btn_quit.clicked.connect(self.onClose)
        #######################################################################

        #################### Video ############################################
        self.image_label = QLabel(self)
        self.disply_width = 640
        self.display_height = 480
        self.image_label.setStyleSheet("background : black;")
        self.layout.addWidget(self.image_label, 0, 0, 8, 8)
        #######################################################################

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
        groupbox_sick = QGroupBox('Состояние')
        groupbox_sick.setLayout(QGridLayout())
        self.layout.addWidget(groupbox_sick, 10, 5, 1, 4)
        self.class_widgets = {}
        for i, class_name in enumerate(self.class_names_ru):
            groupbox_sick.layout().addWidget(QLabel(class_name), x + i, 0, 1, 3)
            self.class_widgets[i] = QLabel('0')
            groupbox_sick.layout().addWidget(self.class_widgets[i], x + i, 4)

        # ######################## Parameters ##################################
        self.operator = QLabel(
            f'Оператор: {self.obj["operator_name"]} {self.obj["operator_patronymic"]} '
            f'{self.obj["operator_surname"]}'
            )
        self.layout.addWidget(self.operator, 0, 8)

        groupbox = QGroupBox('Параметры')
        groupbox.setLayout(QGridLayout())
        self.layout.addWidget(groupbox, 1, 8)

        groupbox.layout().addWidget(QLabel('Сорт картофеля'), 0, 0)
        self.widget_botanical_variety = QComboBox()
        # self.widget_botanical_variety = QLineEdit(self, placeholderText='Название сорта картофеля')
        nomenclatures = ParameterService.get_nomenclatures()
        print(f'nomenclatures={nomenclatures}')
        for i, nomenclature in enumerate(nomenclatures):
            self.widget_botanical_variety.addItem(nomenclature, i)
        self.widget_botanical_variety.setEditable(True)
        groupbox.layout().addWidget(self.widget_botanical_variety, 0, 1)

        groupbox.layout().addWidget(QLabel('Заявленный объём'), 1, 0)
        self.widget_declared_volume = QSpinBox(value=1, maximum=100, minimum=1, singleStep=1)
        groupbox.layout().addWidget(self.widget_declared_volume, 1, 1)

        groupbox.layout().addWidget(QLabel('Транспортное средство'), 2, 0)
        self.widget_truck = QComboBox()
        # self.widget_truck = QLineEdit(self, placeholderText='Марка автомобиля')
        brands, models, gosnumbers = ParameterService.get_cars()
        # for i, car in enumerate(self.obj['cars']):
        for i, (brand, model) in enumerate(zip(brands, models)):
            # self.widget_truck.addItem(f'{car["brand"]} {car["model"]}', i)
            self.widget_truck.addItem(f'{brand} {model}', i)
        self.widget_truck.setEditable(True)
        groupbox.layout().addWidget(self.widget_truck, 2, 1)

        groupbox.layout().addWidget(QLabel('Гос. номер'), 3, 0)
        # self.widget_gosnomer = QLineEdit(self, placeholderText='Гос. номер автомобиля')
        self.widget_gosnomer = QComboBox()
        for i, gosnumber in enumerate(gosnumbers):
            self.widget_gosnomer.addItem(f'{gosnumber}', i)
        self.widget_gosnomer.setEditable(True)
        groupbox.layout().addWidget(self.widget_gosnomer, 3, 1)

        groupbox.layout().addWidget(QLabel('Поставщик'), 4, 0)
        self.widget_provider = QComboBox()
        # self.widget_provider = QLineEdit(self, placeholderText='Название компании')
        self.widget_provider.setEditable(True)
        groupbox.layout().addWidget(self.widget_provider, 5, 1)

        providers = ParameterService.get_providers()
        for i, provider in enumerate(providers):
            self.widget_provider.addItem(provider, i)

        groupbox.layout().addWidget(QLabel('Получатель'), 5, 0)
        self.widget_recipient = QComboBox()
        self.widget_recipient.setEditable(True)
        groupbox.layout().addWidget(self.widget_recipient, 4, 1)

        groupbox.layout().addWidget(QLabel('Направление'), 6, 0)
        self.widget_direction = QComboBox()
        self.widget_direction.addItem('Приёмка', 0)
        self.widget_direction.addItem('Отгрузка', 1)
        groupbox.layout().addWidget(self.widget_direction, 6, 1)

        # ------------- check box -----------------------------
        self.chk_video = QCheckBox(self)
        self.chk_video.setText('Запись видео')
        self.layout.addWidget(self.chk_video, 11, 1)
        self.chk_video.clicked.connect(self.onVideo)

        # Status bar
        self.status = QStatusBar()
        self.status.setStyleSheet("background : lightblue;")  # Setting style sheet to the status bar
        self.setStatusBar(self.status)  # Adding status bar to the main window
        self.status.showMessage('Готово к работе...')

        # dashboard_data = self.hr.get_check_dashboard(self.obj['user_token'], self.obj['current_client'])
        recipient = ParameterService.get_recipient()
        if recipient is not None:
            print(f'recipient={recipient}')
            self.widget_recipient.addItem(recipient, 0)

    def initMenu(self):
        menuBar = self.menuBar()
        users = menuBar.addMenu('Пользователи')
        usersAction = QAction('Сменить оператора', self)
        usersAction.setStatusTip('Сменить оператора в текущей сессии')
        usersAction.triggered.connect(self.onChangeUser)
        users.addAction(usersAction)

        parameters = menuBar.addMenu('Параметры')
        deviceAction = QAction('Периферийные устройства..', self)
        deviceAction.setStatusTip('Настройка периферийного устройства', )
        deviceAction.triggered.connect(self.onDevice)

        nnAction = QAction('Нейронной сети..', self)
        nnAction.triggered.connect(self.onNn)
        nnAction.setStatusTip('Настройка параметров нейронной сети', )

        checklinkAction = QAction('Проверка связи с сервером..', self)
        checklinkAction.triggered.connect(self.onCheckLink)
        checklinkAction.setStatusTip('Проверка связи с сервером')

        parameters.addActions([checklinkAction, deviceAction, nnAction])

    ######################################################################
    #                                   Events                           #
    ######################################################################
    def onChangeUser(self):
        old_operator_id = self.obj['operator_id']
        self.obj['password'] = '0'
        print(f'old_operator_id={old_operator_id}')
        lw = LoginWindow(self.obj)
        lw.exec()
        print(f'self.obj={self.obj}')
        new_operator_id = self.obj['operator_id']
        print(f'new_operator_id={new_operator_id}')
        if new_operator_id == old_operator_id:
            QMessageBox.warning(self, 'Предупреждение', 'Пользователь не сменен.')
        else:
            QMessageBox.information(self, 'Информация', 'Пользователь сменен.')
            self.operator.setText( f'Оператор: {self.obj["operator_name"]} {self.obj["operator_patronymic"]} '
            f'{self.obj["operator_surname"]}')
        if self.obj['password'] == '0':
            QMessageBox.warning(self, 'Предупреждение', 'Пользователь ввёл не правильный пароль.')

    def onCheckLink(self):
        cl = ChecklinkWindow()
        cl.exec()

    def onClose(self):
        self.thread.stop()
        self.close()

    def onClear(self):
        self.btn_http.setEnabled(False)
        self.result.setText("0")
        self.big_size.setText("0")
        self.middle_size.setText("0")
        self.small_size.setText("0")

        self.rd.total_count = "0"
        self.rd.large_caliber = "0"
        self.rd.medium_caliber = "0"
        self.rd.small_caliber = "0"
        for i, class_name in enumerate(self.class_names_ru):
            self.class_widgets[i].setText("0")

        self.status.showMessage('Данные очищены')

    def onDevice(self):
        d = DeviceWindow()
        d.exec()

    def onNn(self):
        n = NnWindow()
        n.exec()

    def onPrint(self):
        pw = PrintWindow(self.obj)
        pw.exec()

    def onRequest(self):
        print(f"obj[token]={self.obj['token']}")
        if self.obj['token'] is None or self.obj['password'] == '0':
            lw = LoginWindow(self.obj)
            lw.exec()
            # self.rd.operator_id = self.obj['operator_id']
            self.fill_from_data()
        print(f'self.rd={self.rd.data}')
        if self.obj['password'] == '1':
            ret = self.hr.send_request(self.obj['token'], self.rd.data)
        else:
            # password is not entered by user
            ret = False
        print(f'ret={ret}')
        if ret:
            send_session_data(self.hr, self.obj)
            QMessageBox.information(self, 'Информация', 'Данные отправлены на Веб сервер.')
        else:
            save_session_data(self.rd)
            QMessageBox.warning(
                self, 'Ошибка', 'Невозможно записать данные на сервер, попробуйте позднее.\nДанные '
                                'будут записаны в БД на диске.\nПри появлении связи, при следующей '
                                'попытки соединении с сервером, эти данные будут записаны на сервер.'
                )

    def onVideo(self):
        if self.save_video:
            self.save_video = False
            self.thread.stop_video()
            # print('Stop video')
        else:
            self.save_video = True
            self.thread.start_video()
            # print('Start video')

    ############################################################################
    #                                    Buttons                               #
    ############################################################################
    # Activates when Start/Stop video button is clicked to Start (ss_video
    def ClickStartVideo(self):
        self.btn_http.setEnabled(True)
        self.rd.start_date = str(datetime.date.today())
        self.rd.start_time = time.strftime('%H:%M', time.localtime())
        # Change label color to light blue
        self.ss_video.clicked.disconnect(self.ClickStartVideo)
        self.status.showMessage('Идёт трансляция...')
        # Change button to stop
        self.ss_video.setText('Пауза')
        # self.thread = VideoThread()
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
        self.rd.botanical_variety = self.widget_botanical_variety.currentText()
        self.rd.declared_volume = str(self.widget_declared_volume.value())
        self.rd.car = self.widget_truck.currentText()
        self.rd.gosnomer = self.widget_gosnomer.currentText()
        self.rd.provider = self.widget_provider.currentText()
        self.rd.recipient = self.widget_recipient.currentText()
        # self.hr.direction = self.widget_direction.currentText()
        self.rd.total_count = str(self.sizes['result'])
        self.rd.large_caliber = str(self.sizes['big'])
        self.rd.medium_caliber = str(self.sizes['middle'])
        self.rd.small_caliber = str(self.sizes['small'])
        ######## classes ####################
        # self.rd.phytophthora=self.class_widgets[7].text()
        self.rd.strong = self.class_widgets[0].text()
        self.rd.rot = self.class_widgets[1].text()
        self.rd.end_date = str(datetime.date.today())
        self.rd.end_time = time.strftime('%H:%M', time.localtime())
        self.status.showMessage('Трансляция остановлена, данные должны быть отправлены на сервер.')

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
        self.image_label.setPixmap(qt_img)  # show video

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

    def fill_from_data(self):
        self.rd.operator_id = self.obj['operator_id']
        self.rd.operator_name = self.obj['operator_name']
        self.rd.operator_surname = self.obj['operator_surname']
        self.rd.operator_patronymic = self.obj['operator_patronymic']
        self.hr(ip_address=self.obj['ip_address'], port=self.obj['port'])


if __name__ == '__main__':
    create_dirs()
    create_db_and_tables()
    app = QApplication(sys.argv)
    # lw = LoginWindow()
    # lw.show()
    # print(lw.token)
    win = MyWindow()
    # win.show()
    sys.exit(app.exec())

import sys
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QTextDocument
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, \
    QPushButton, \
    QTextEdit, QVBoxLayout, QWidget

from classes.http_request import HttpRequest
from db.services.option_service import OptionService


class PrintWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Печать документов')
        self.switched = False
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyZWNmNjhlOWMyZjlmNzJiMGQ5ODlkZCIsIm5iZiI6MTY1OTY5NjgzNSwiZXhwIjoyMTIzMjMyODM1LCJpc3MiOiJNeUF1dGhTZXJ2ZXIiLCJhdWQiOiJNeUF1dGhTZXJ2ZXIifQ.RDvIfJ8qEXqh-pEozX0hzAHhsjMfNMQgQoB13gAq_Kg'  #OptionService.get_option(['token'])
        self.ip_address ='erp.bk-nt.ru' # OptionService.get_option(['server_address'])
        self.invoice_view = None
        self.initWindow()

    def initWindow(self):
        print('initWindow')
        # set layout
        self.layout = QHBoxLayout(self)

        group_main = QGroupBox()
        group_main.setLayout(QVBoxLayout())
        self.layout.addWidget(group_main)

        group_doc = QGroupBox('Выбор документов')
        group_doc.setLayout(QVBoxLayout())
        # group_doc.setAlignment(Qt.AlignTop)
        self.doc_cb = QComboBox()

        group_doc.layout().addWidget(self.doc_cb)
        doc_btn = QPushButton('Выбрать..')
        group_doc.layout().addWidget(doc_btn, alignment=Qt.AlignTop)
        doc_btn.clicked.connect(self.onShowDocument)
        group_main.layout().addWidget(group_doc)

        group_preview = QGroupBox('Принтер')
        group_preview.setLayout(QVBoxLayout())
        group_main.layout().addWidget(group_preview)

        self.invoice_view = InvoiceView()
        self.layout.addWidget(self.invoice_view)
        # self.invoice_view.build_invoice('<p>p</p>')

        self.documents = self.get_analisis_list()
        for i, document in enumerate(self.documents):
            self.doc_cb.addItem(f'№ {document["number"]} от {document["start_date"]} {document["start_time"]}', i)


    def get_analisis_list(self) -> List:
        print(f'self.ip_address={self.ip_address}')
        print(f'self.token={self.token}')
        hr = HttpRequest(ip_address=self.ip_address)
        # d = hr.get_check(self.token)
        # print(f'd={d}')
        _data = {}
        _data["page"]="1"
        _data["limit"] = "10"
        _data["exclude_type"] = "4"
        print(f'_data={_data}')
        # data =hr.get_analisis_list(self.token, {'page': '1', 'limit': '10', 'exclude_type': '4'})
        response = hr.get_analisis_list(
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyZWNmMzA0OWMyZjlmNzJiMGQ5ODljYiIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL25hbWUiOiLQkNC00LzQuNC90LjRgdGC0YDQsNGC0L7RgCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6ImFkbWluIiwibmJmIjoxNjY5OTg1MjE1LCJleHAiOjE2NzAwNzE2MTUsImlzcyI6Ik15QXV0aFNlcnZlciIsImF1ZCI6Ik15QXV0aFNlcnZlciJ9.fqIsNdVPNpxefemBT-ECcPOVuENtp88BJJ5ogdtGJtM'
                                    , _data)

        data_list = []
        # print(f'data={response["data"]}')
        if response is not None:
            for item in response["data"]:
                data = {}
                print(f'start_date={item["start_date"]}')
                data['document'] = item['document']
                data['id'] = item['id']
                data['number'] = item['number']
                data['start_date'] = item['start_date']
                data['start_time'] = item['start_time']
                data_list.append(data)
        # print(f'data_list={data_list}')
        return data_list

    def onShowDocument(self):
        index = self.doc_cb.currentIndex()
        self.invoice_view.build_invoice(self.documents[index]['document'])




class InvoiceView(QTextEdit):

    dpi = 72
    doc_width = 8.5 * dpi
    doc_height = 11 * dpi

    def __init__(self):
        super().__init__(readOnly=True)
        # self.setFixedSize(qtc.QSize(self.doc_width, self.doc_height))

    def build_invoice(self, data):
        document = QTextDocument()
        self.setDocument(document)
        cursor = QTextCursor(document)
        root = document.rootFrame()
        cursor.setPosition(root.lastPosition())
        cursor.insertHtml(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PrintWindow()
    win.show()
    sys.exit(app.exec())


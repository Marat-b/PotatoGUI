import sys
from typing import List

from PyQt5.QtCore import QDir, QSize, QSizeF, Qt
from PyQt5.QtGui import QPageSize, QTextCursor, QTextDocument
from PyQt5.QtPrintSupport import QPageSetupDialog, QPrintDialog, QPrintPreviewDialog, QPrinter
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, \
    QLabel, \
    QPushButton, \
    QSpinBox, QTextEdit, QVBoxLayout, QWidget

from classes.http_request import HttpRequest
from utils.utils import utc_str_to_local_str


class PrintWindow(QDialog):
    # dpi = 72
    # doc_width = 8.5 * dpi
    # doc_height = 11 * dpi
    def __init__(self, data, parent=None):
        super().__init__(parent)
        # self.setFixedSize(QSize(self.doc_width, self.doc_height))
        self._data = data
        print(f'PrintWindow data={self._data}')
        self.setWindowTitle('Печать документов')
        self.switched = False
        self.token = self._data['token']
        self.ip_address = self._data['ip_address']
        self.invoice_view = None

        self.initWindow()

    def initWindow(self):
        print('initWindow')
        self.preview = InvoiceView()
        # set layout
        self.layout = QHBoxLayout(self)

        group_main = QGroupBox()
        group_main.setLayout(QVBoxLayout())
        self.layout.addWidget(group_main, alignment=Qt.AlignTop)

        group_doc = QGroupBox('Выбор документов')
        group_doc.setLayout(QVBoxLayout())
        # group_doc.setAlignment(Qt.AlignTop)

        group_doc.layout().addWidget(QLabel('Получить последние N док-в'))

        self.field_ndocs = QSpinBox(value=5, maximum=50, minimum=1, singleStep=1)
        group_doc.layout().addWidget(self.field_ndocs)

        btn_refresh_list = QPushButton('Обновить')
        group_doc.layout().addWidget(btn_refresh_list, alignment=Qt.AlignTop)
        btn_refresh_list.clicked.connect(self.onRefreshList)

        self.doc_cb = QComboBox()

        group_doc.layout().addWidget(self.doc_cb)
        doc_btn = QPushButton('Выбрать..')
        group_doc.layout().addWidget(doc_btn, alignment=Qt.AlignTop)
        doc_btn.clicked.connect(self.onShowDocument)
        group_main.layout().addWidget(group_doc, alignment=Qt.AlignTop)

        ############ Printer ########################
        self.printer = QPrinter()
        self.printer.setOrientation(QPrinter.Portrait)
        self.printer.setPageSize(QPageSize(QPageSize.A4))

        group_preview = QGroupBox('Принтер')
        group_preview.setLayout(QVBoxLayout())
        group_main.layout().addWidget(group_preview, alignment=Qt.AlignTop)

        btn_config = QPushButton('Конфигурация')
        btn_config.clicked.connect(self.onConfig)
        group_preview.layout().addWidget(btn_config, alignment=Qt.AlignTop)

        btn_preview = QPushButton('Просмотр')
        btn_preview.clicked.connect(self.onPreview)
        group_preview.layout().addWidget(btn_preview)

        btn_print = QPushButton('Печать')
        btn_print.clicked.connect(self.onPrint)
        group_preview.layout().addWidget(btn_print)

        btn_export = QPushButton('Сохранить в PDF')
        btn_export.clicked.connect(self.onExport)
        group_preview.layout().addWidget(btn_export)

        btn_close = QPushButton('Выйти')
        btn_close.clicked.connect(self.onClose)
        group_main.layout().addWidget(btn_close)

        self.layout.addWidget(self.preview)
        # self.invoice_view.build_invoice('<p>p</p>')

        self.documents = self.get_analisis_list(self.field_ndocs.text())
        for i, document in enumerate(self.documents):
            self.doc_cb.addItem(f'№ {document["number"]} от {document["start_date"]} {document["start_time"]}', i)

        self._update_preview_size()

    def get_analisis_list(self, limit) -> List:
        print(f'self.ip_address={self.ip_address}')
        print(f'self.token={self.token}')
        hr = HttpRequest(ip_address=self.ip_address)
        # d = hr.get_check(self.token)
        # print(f'd={d}')
        _data = {}
        _data["page"] = "1"
        _data["limit"] = limit
        _data["exclude_type"] = "4"
        print(f'_data={_data}')
        # data =hr.get_analisis_list(self.token, {'page': '1', 'limit': '10', 'exclude_type': '4'})
        response = hr.get_analisis_list(
            self._data['token'],
             _data
        )

        data_list = []
        # print(f'data={response["data"]}')
        if response is not None:
            for item in response["data"]:
                data = {}
                # print(f'start_date={item["start_date"]}')
                data['document'] = item['document']
                data['id'] = item['id']
                data['number'] = item['number']
                data['start_date'] = utc_str_to_local_str(item['start_date'])
                data['start_time'] = item['start_time']
                data_list.append(data)
        # print(f'data_list={data_list}')
        return data_list

    def _print_document(self):
        # doesn't actually kick off printer,
        # just paints document to the printer object
        self.preview.document().print(self.printer)

    def _update_preview_size(self):
        self.preview.set_page_size(
            self.printer.pageRect(QPrinter.Point)
        )

    ############### Events #########################
    def onClose(self):
        self.close()

    def onConfig(self):
        dialog = QPageSetupDialog(self.printer, self)
        dialog.exec()
        self._update_preview_size()

    def onExport(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Сохранить в PDF", QDir.homePath(), "PDF файлы (*.pdf)"
        )
        if filename:
            self.printer.setOutputFileName(filename)
            self.printer.setOutputFormat(QPrinter.PdfFormat)
            self._print_document()

    def onPrint(self):
        # Errata:  the book contained this line:
        # self._print_document()
        # As noted by DevinLand in issue #8, this can cause the document to start printing.
        dialog = QPrintDialog(self.printer, self)

        # Instead we'll add this line, so _print_document is triggered when the dialog is
        # accepted:
        dialog.accepted.connect(self._print_document)
        dialog.exec()
        self._update_preview_size()

    def onPreview(self):
        dialog = QPrintPreviewDialog(self.printer, self)
        dialog.paintRequested.connect(self._print_document)
        dialog.exec()
        self._update_preview_size()

    def onRefreshList(self):
        self.documents = self.get_analisis_list(self.field_ndocs.text())
        self.doc_cb.clear()
        for i, document in enumerate(self.documents):
            self.doc_cb.addItem(f'№ {document["number"]} от {document["start_date"]} {document["start_time"]}', i)

    def onShowDocument(self):
        index = self.doc_cb.currentIndex()
        self.preview.build_invoice(self.documents[index]['document'])


class InvoiceView(QTextEdit):

    dpi = 72
    doc_width = 8.3 * dpi
    doc_height = 11.7 * dpi

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

    def set_page_size(self, qrect):
        self.doc_width = qrect.width()
        self.doc_height = qrect.height()
        self.setFixedSize(QSize(self.doc_width, self.doc_height))
        self.document().setPageSize(
            QSizeF(self.doc_width, self.doc_height)
        )


if __name__ == '__main__':
    data = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' \
                 '.eyJpZCI6IjYyZWNmNjhlOWMyZjlmNzJiMGQ5ODlkZCIsIm5iZiI6MTY1OTY5NjgzNSwiZXhwIjoyMTIzMjMyODM1LCJpc3MiOiJNeUF1dGhTZXJ2ZXIiLCJhdWQiOiJNeUF1dGhTZXJ2ZXIifQ.RDvIfJ8qEXqh-pEozX0hzAHhsjMfNMQgQoB13gAq_Kg',
        'ip_address': 'erp.bk-nt.ru',
        'user_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
            '.eyJpZCI6IjYyZWNmMzA0OWMyZjlmNzJiMGQ5ODljYiIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL25hbWUiOiLQkNC00LzQuNC90LjRgdGC0YDQsNGC0L7RgCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6ImFkbWluIiwibmJmIjoxNjcwMDgxNDY0LCJleHAiOjE2NzAxNjc4NjQsImlzcyI6Ik15QXV0aFNlcnZlciIsImF1ZCI6Ik15QXV0aFNlcnZlciJ9.UcVSjHfUPbW0UWGBHsKSlSGG0d0y1yOeI4_nArPAxl8'
        }


    app = QApplication(sys.argv)
    win = PrintWindow(data)
    win.show()
    sys.exit(app.exec())

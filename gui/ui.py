# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot, QThreadPool
import threading

from atcrawl.gui.welcome_design import *
from atcrawl.gui.crawler_design import *
from atcrawl.crawlers import *


def show_popup(main_text, info='', icon=QMessageBox.Information):
    msg = QMessageBox()
    msg.setWindowTitle("atCrawl Dialog")
    msg.setText(main_text)
    msg.setIcon(icon)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.setInformativeText(info)
    msg.exec_()


class WelcomeUI(Ui_WelcomeUI):
    def __init__(self, window):
        self.setupUi(window)
        self.ui = None

        self.bt_antallaktika.clicked.connect(
            lambda: self.init_crawler("antallaktikaonline.gr"))
        self.bt_skroutz.clicked.connect(
            lambda: self.init_crawler("skroutz.gr"))
        self.bt_booking.clicked.connect(
            lambda: self.init_crawler("booking.com"))
        self.bt_tripadvisor.clicked.connect(
            lambda: self.init_crawler("tripadvisor.com"))
        self.bt_spitogatos.clicked.connect(
            lambda: self.init_crawler("spitogatos.gr"))

    def init_crawler(self, name):
        authorizer = Authorize(name)
        if authorizer.user_is_licensed():
            self.ui = CrawlerUI()
            self.ui.set_crawler(crawler_map[name]())
            self.ui.set_auth(authorizer)
            self.ui.apply_masks()
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support")


class Worker(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)


class CrawlerUI(QMainWindow, Ui_CrawlerUI):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.crawler: CrawlEngine = CrawlEngine('None')
        self.auth = None

        self.url = None
        self.old_url = None
        self.brand = None
        self.discount = None
        self.file_name = None
        self.folder_name = None
        self.driver_status = False
        self.to_export = False
        self.nitems = 0

        self.worker = None
        self.threadpool = QThreadPool()
        self.event_stop = threading.Event()

        self.in_folder.setText(paths.get_default_export())

        self.bt_launch.clicked.connect(self.launch)
        self.bt_terminate.clicked.connect(self.terminate)
        self.bt_collect.clicked.connect(self.collect_thread_start)
        self.bt_stop_collect.clicked.connect(self.collect_thread_stop)
        self.bt_reset.clicked.connect(self.reset)
        self.bt_export.clicked.connect(self.export)
        self.browse_folder.clicked.connect(self.folder)

    def apply_masks(self):
        if self.crawler.NAME == 'antallaktikaonline.gr':
            self.in_meta1.setStyleSheet(
                "background-color: rgba(112, 112, 112, 0.8);\n"
                "border-width:4px;\n"
                "border-color:black;\n"
                "border-style:offset;\n"
                "border-radius:10px;")
            self.in_meta2.setStyleSheet(
                "background-color: rgba(112, 112, 112, 0.8);\n"
                "border-width:4px;\n"
                "border-color:black;\n"
                "border-style:offset;\n"
                "border-radius:10px;")
            self.in_meta3.setStyleSheet(
                "background-color: rgba(112, 112, 112, 0.8);\n"
                "border-width:4px;\n"
                "border-color:black;\n"
                "border-style:offset;\n"
                "border-radius:10px;")

            self.label_meta0.setText("Car")
        if self.crawler.NAME == 'skroutz.gr':
            self.label_meta0.setText('ID Category')
            self.label_meta1.setText('Description')
            self.label_meta2.setText('Meta Title SEO')
            self.label_meta3.setText("Meta SEO")

    def show_output(self, text=''):
        self.output.setText(text)
        self.output.setStyleSheet(
            "background-color: rgba(80, 244, 20, 0.8);\n"
            "border-width:4px;\n"
            "border-color:black;\n"
            "border-style:offset;\n"
            "border-radius:10px;")

    def mask_output(self):
        self.output.setText('')
        self.output.setStyleSheet(
            "background-color: rgba(112, 112, 112, 0.8);\n"
            "border-width:4px;\n"
            "border-color:black;\n"
            "border-style:offset;\n"
            "border-radius:10px;")

    def change_browser_status(self, status):
        if status == 'online':
            self.status_browser.setText(status)
            self.status_browser.setStyleSheet(
                "background-color: rgba(80, 244, 20, 0.8);\n"
                "border-width:4px;\n"
                "border-color:black;\n"
                "color: rgb(0, 0, 0);\n"
                "border-style:offset;\n"
                "border-radius:10px;")
        else:
            self.status_browser.setText(status)
            self.status_browser.setStyleSheet(
                "background-color: rgba(253, 4, 50, 0.8);\n"
                "border-width:4px;\n"
                "border-color:black;\n"
                "color: rgb(0, 0, 0);\n"
                "border-style:offset;\n"
                "border-radius:10px;")

    def change_crawler_status(self, status):
        if status == 'running':
            self.status_crawler.setText(status)
            self.status_crawler.setStyleSheet(
                "background-color: rgba(80, 244, 20, 0.8);\n"
                "border-width:4px;\n"
                "border-color:black;\n"
                "color: rgb(0, 0, 0);\n"
                "border-style:offset;\n"
                "border-radius:10px;")
        elif status == 'offline':
            self.status_crawler.setText(status)
            self.status_crawler.setStyleSheet(
                "background-color: rgba(253, 4, 50, 0.8);\n"
                "border-width:4px;\n"
                "border-color:black;\n"
                "color: rgb(0, 0, 0);\n"
                "border-style:offset;\n"
                "border-radius:10px;")
        else:
            self.status_crawler.setText(status)
            self.status_crawler.setStyleSheet(
                "background-color: rgba(208, 243, 33, 0.8);\n"
                "border-width:4px;\n"
                "border-color:black;\n"
                "color: rgb(0, 0, 0);\n"
                "border-style:offset;\n"
                "border-radius:10px;")

    def count_parsed(self):
        dd = self.crawler.data
        self.nitems = str(len(dd[list(dd.keys())[0]]))
        return self.nitems

    def set_crawler(self, crawler_obj):
        self.crawler = crawler_obj

    def set_auth(self, authorizer):
        self.auth = authorizer

    def folder(self):
        folder = QFileDialog.getExistingDirectory()

        if folder:
            self.in_folder.setText(folder)
            self.folder_name = folder

    def get_folder(self):
        _folder = self.in_folder.text()

        if _folder == '':
            self.folder_name = paths.get_cwd()
        else:
            self.folder_name = _folder

        return self.folder_name

    def get_filename(self):
        _filename = self.in_filename.text()
        if _filename == '':
            self.file_name = 'Collected_Data'
        else:
            self.file_name = _filename

        return self.file_name

    def get_discount(self):
        _discount = self.in_discount.text()
        if _discount == '':
            self.discount = 0
        else:
            self.discount = int(_discount)
        return self.discount

    def get_brand(self):
        self.brand = self.in_brand.text()
        return self.brand

    def get_params(self):
        _params = {'meta0': self.in_meta0.text(),
                   'meta1': self.in_meta1.text(),
                   'meta2': self.in_meta2.text(),
                   'meta3': self.in_meta3.text(),
                   'brand': self.get_brand(),
                   'discount': self.get_discount()}

        return _params

    def launch(self):
        self.url = self.in_url.text()
        self.old_url = self.in_url.text()

        if self.url is not None and self.url != '':
            self.crawler.set_url(self.url)
            self.crawler.launch('Chrome', paths.get_chrome())
            self.driver_status = True

            self.change_browser_status("online")
            self.change_crawler_status('idle')
            self.bt_launch.setEnabled(False)

            if self.check_launch_collect.isChecked():
                self.collect_thread_start()
        else:
            show_popup("URL is not set. Launch cancelled!",
                       "Set the url and then launch.",
                       QMessageBox.Critical)

    def collect(self):
        self.bt_collect.setEnabled(False)
        self.bt_reset.setEnabled(False)

        self.change_crawler_status('running')
        self.mask_output()

        self.event_stop.clear()
        self.crawler.pre_collect()

        while not self.event_stop.is_set() and self.crawler.click('Next'):
            self.crawler.collect(gather='single')

        self.bt_collect.setEnabled(True)
        self.bt_reset.setEnabled(True)

        if self.crawler.NAME == "antallaktikaonline.gr":
            self.crawler.parse()

        self.count_items.setText(self.count_parsed())
        self.change_crawler_status('idle')
        self.event_stop.set()
        self.to_export = True
        if self.check_export.isChecked():
            self.export()

    @QtCore.pyqtSlot()
    def collect_thread_start(self):
        if self.driver_status:
            if self.auth.user_is_licensed():
                worker = Worker(self.collect)
                self.threadpool.start(worker)
            else:
                show_popup("You are not authorized",
                           "Contact support",
                           QMessageBox.Information)
        else:
            show_popup("Launch the driver first!")

    @QtCore.pyqtSlot()
    def collect_thread_stop(self):
        self.event_stop.set()

    def export(self):
        if self.to_export:
            if self.auth.user_is_licensed():
                _name = self.get_filename()
                _folder = self.get_folder()
                _type = self.list_type.currentText()

                self.crawler.transform(**self.get_params())

                self.crawler.export(name=_name,
                                    folder=_folder,
                                    export_type=_type)

                _pre = "Generated file --> "
                _output = _folder + '\\' + _name
                self.show_output(_pre + _output)

                self.to_export = False
            else:
                show_popup("You are not authorized",
                           "Contact support",
                           QMessageBox.Information)
        else:
            show_popup("Nothing to export")

    def reset(self):
        if self.driver_status:
            _url = self.in_url.text()

            if _url == self.old_url:
                self.crawler.reset()
            else:
                self.crawler.reset(_url)
                self.old_url = _url

            self.to_export = False
            self.count_items.setText(self.count_parsed())
        else:
            show_popup("Launch the driver first!")

    def terminate(self):
        if self.driver_status:
            self.crawler.terminate()
            self.driver_status = False
            self.change_browser_status("offline")
            self.change_crawler_status("offline")
            self.bt_launch.setEnabled(True)
        else:
            show_popup("Launch the driver first!")


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    welcome_ui = WelcomeUI(main_window)
    main_window.show()
    sys.exit(app.exec_())

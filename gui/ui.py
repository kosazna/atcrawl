# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from atcrawl.gui.welcome_design import *
from atcrawl.gui.crawler_design import *
from atcrawl.utilities.auth import *

auth = Authorize()


def show_popup(main_text, info, icon):
    msg = QMessageBox()
    msg.setWindowTitle("atCrawl")
    msg.setText(main_text)
    msg.setIcon(icon)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.setInformativeText(info)
    popup = msg.exec_()


class WelcomeUI(Ui_WelcomeUI):
    def __init__(self, window):
        self.setupUi(window)
        self.ui = None

        self.bt_antallaktika.clicked.connect(self.start_antallaktika)
        self.bt_skroutz.clicked.connect(self.start_skroutz)
        self.bt_booking.clicked.connect(self.start_booking)
        self.bt_tripadvisor.clicked.connect(self.start_tripadvisor)
        self.bt_spitogatos.clicked.connect(self.start_spitogatos)

    def start_antallaktika(self):
        if auth.user_is_licensed('antallaktikaonline.gr'):
            self.ui = CrawlerUI()
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support",
                       QMessageBox.Information)

    def start_skroutz(self):
        if auth.user_is_licensed('skroutz.gr'):
            self.ui = CrawlerUI()
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support",
                       QMessageBox.Information)

    def start_booking(self):
        if auth.user_is_licensed('booking.com'):
            self.ui = CrawlerUI()
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support",
                       QMessageBox.Information)

    def start_tripadvisor(self):
        if auth.user_is_licensed('tripadvisor.gr'):
            self.ui = CrawlerUI()
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support",
                       QMessageBox.Information)

    def start_spitogatos(self):
        if auth.user_is_licensed('spitogatos.gr'):
            self.ui = CrawlerUI()
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support",
                       QMessageBox.Information)


class CrawlerUI(QMainWindow, Ui_CrawlerUI):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.crawler = None
        self.paths = None
        self.log = None
        self.auth = None

        self.url = None
        self.brand = None
        self.discount = None
        self.filename_name = None
        self.folder_name = None

        self.bt_launch.clicked.connect(self.launch)
        # self.bt_terminate.clicked.connect()
        self.bt_collect.clicked.connect(self.collect)
        # self.bt_reset.clicked.connect()
        self.bt_launch_collect.clicked.connect(self.launch_collect)
        # self.bt_reset_collect.clicked.connect()
        self.bt_export.clicked.connect(self.export)
        self.browse_folder.clicked.connect(self.folder)

        # self.check_export.stateChanged.connect()

    def set_crawler(self, crawler):
        self.crawler = crawler

    def set_paths(self, paths):
        self.paths = paths

    def set_logger(self, logger):
        self.log = logger

    def set_auth(self, auth):
        self.auth = auth

    def folder(self):
        folder = QFileDialog.getExistingDirectory()

        if folder:
            self.in_folder.setText(folder)
            self.folder_name = folder

    def get_discount(self):
        _discount = self.in_discount.text()
        if _discount == '':
            self.discount = 0
        else:
            self.discount = int(_discount)

    def get_brand(self):
        self.brand = self.in_brand.text()

    def launch(self):
        self.url = self.in_url.text()

        if self.url is not None and self.url != '':
            self.crawler.set_url(self.url)
            self.crawler.launch('Chrome', self.paths.get_chrome())

            self.status.setText("online")
            self.status.setStyleSheet(
                "background-color: rgba(80, 244, 20, 0.8);\n"
                "border-width:4px;\n"
                "border-color:black;\n"
                "color: rgb(0, 0, 0);\n"
                "border-style:offset;\n"
                "border-radius:10px;")
        else:
            show_popup("URL is not set",
                       "Set the url and then launch",
                       QMessageBox.Critical)

    def launch_collect(self):
        self.url = self.in_url.text()

        if self.url is not None and self.url != '':
            self.crawler.set_url(self.url)
            self.crawler.launch('Chrome', self.paths.get_chrome())

            self.status.setText("online")
            self.status.setStyleSheet(
                "background-color: rgba(80, 244, 20, 0.8);\n"
                "border-width:4px;\n"
                "border-color:black;\n"
                "color: rgb(0, 0, 0);\n"
                "border-style:offset;\n"
                "border-radius:10px;")

            self.crawler.collect()
        else:
            show_popup("URL is not set",
                       "Set the url and then launch",
                       QMessageBox.Critical)

    def collect(self):
        self.crawler.collect()

    def export(self):
        _name = self.in_filename.text()
        _folder = self.in_folder.text()

        self.crawler.transform(brand=self.brand,
                               discount=self.discount)

        self.crawler.export(name=_name, folder=_folder)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    welcome_ui = WelcomeUI(main_window)
    main_window.show()
    sys.exit(app.exec_())

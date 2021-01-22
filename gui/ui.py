# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox
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

        self.bt_antallaktika.clicked.connect(self.start_antallaktika)
        self.bt_skroutz.clicked.connect(self.start_skroutz)
        self.bt_booking.clicked.connect(self.start_booking)
        self.bt_tripadvisor.clicked.connect(self.start_tripadvisor)
        self.bt_spitogatos.clicked.connect(self.start_spitogatos)

    def start_antallaktika(self):
        authorizer = Authorize('antallaktikaonline.gr')
        if authorizer.user_is_licensed():
            self.ui = CrawlerUI()
            self.ui.set_crawler(AntallaktikaOnline())
            self.ui.set_auth(authorizer)
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support")

    def start_skroutz(self):
        authorizer = Authorize('skroutz.gr')
        if authorizer.user_is_licensed():
            self.ui = CrawlerUI()
            self.ui.set_crawler(Skroutz())
            self.ui.set_auth(authorizer)
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support")

    def start_booking(self):
        authorizer = Authorize('booking.com')
        if authorizer.user_is_licensed():
            self.ui = CrawlerUI()
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support")

    def start_tripadvisor(self):
        authorizer = Authorize('tripadvisor.com')
        if authorizer.user_is_licensed():
            self.ui = CrawlerUI()
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support")

    def start_spitogatos(self):
        authorizer = Authorize('spitogatos.gr')
        if authorizer.user_is_licensed():
            self.ui = CrawlerUI()
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support")


class CrawlerUI(QMainWindow, Ui_CrawlerUI):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.crawler = None
        self.auth = None

        self.url = None
        self.brand = None
        self.discount = None
        self.file_name = None
        self.folder_name = None
        self.driver_status = False
        self.to_export = False

        self.bt_launch.clicked.connect(self.launch)
        self.bt_terminate.clicked.connect(self.terminate)
        self.bt_collect.clicked.connect(self.collect)
        self.bt_reset.clicked.connect(self.reset)
        self.bt_launch_collect.clicked.connect(self.launch_collect)
        self.bt_reset_collect.clicked.connect(self.reset_collect)
        self.bt_export.clicked.connect(self.export)
        self.browse_folder.clicked.connect(self.folder)

        # self.check_export.stateChanged.connect()

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
        self.folder_name = _folder

        return self.folder_name

    def get_filename(self):
        _filename = self.in_filename.text()
        if _filename == '':
            self.file_name = 'Collected_Data'
        self.file_name = _filename

        return self.file_name

    def get_discount(self):
        _discount = self.in_discount.text()
        if _discount == '':
            self.discount = 0
        self.discount = int(_discount)
        return self.discount

    def get_brand(self):
        self.brand = self.in_brand.text()
        return self.brand

    def launch(self):
        self.url = self.in_url.text()

        if self.url is not None and self.url != '':
            self.crawler.set_url(self.url)
            self.crawler.launch('Chrome', paths.get_chrome())
            self.driver_status = True

            self.status.setText("online")
            self.status.setStyleSheet(
                "background-color: rgba(80, 244, 20, 0.8);\n"
                "border-width:4px;\n"
                "border-color:black;\n"
                "color: rgb(0, 0, 0);\n"
                "border-style:offset;\n"
                "border-radius:10px;")
        else:
            show_popup("URL is not set. Launch cancelled !",
                       "Set the url and then launch.",
                       QMessageBox.Critical)

    def launch_collect(self):
        if self.auth.user_is_licensed():
            self.url = self.in_url.text()

            if self.url is not None and self.url != '':
                self.crawler.set_url(self.url)
                self.crawler.launch('Chrome', self.paths.get_chrome())
                self.driver_status = True

                self.status.setText("online")
                self.status.setStyleSheet(
                    "background-color: rgba(80, 244, 20, 0.8);\n"
                    "border-width:4px;\n"
                    "border-color:black;\n"
                    "color: rgb(0, 0, 0);\n"
                    "border-style:offset;\n"
                    "border-radius:10px;")

                self.collect()
                self.to_export = True

                if self.check_export.isChecked():
                    self.export()
            else:
                show_popup("URL is not set. Launch cancelled !",
                           "Set the url and then launch.",
                           QMessageBox.Critical)
        else:
            show_popup("You are not authorized",
                       "Contact support",
                       QMessageBox.Information)

    def collect(self):
        if self.driver_status:
            if self.auth.user_is_licensed():
                self.crawler.collect()
                self.to_export = True

                if self.check_export.isChecked():
                    self.export()
            else:
                show_popup("You are not authorized",
                           "Contact support",
                           QMessageBox.Information)
        else:
            show_popup("Launch the driver first!")

    def export(self):
        if self.to_export:
            if self.auth.user_is_licensed():
                _name = self.get_filename()
                _folder = self.get_folder()
                _type = self.list_type.currentText()

                self.crawler.transform(brand=self.get_brand(),
                                       discount=self.get_discount())

                self.crawler.export(name=_name,
                                    folder=_folder,
                                    export_type=_type)
            else:
                show_popup("You are not authorized",
                           "Contact support",
                           QMessageBox.Information)
        else:
            show_popup("Nothing to export")

    def reset(self):
        if self.driver_status:
            _url = self.in_url.text()

            if self.url == _url:
                self.crawler.reset()
            else:
                self.crawler.reset(_url)

            self.to_export = False
        else:
            show_popup("Launch the driver first!")

    def reset_collect(self):
        if self.driver_status:
            if self.auth.user_is_licensed():
                self.reset()
                self.collect()
            else:
                show_popup("You are not authorized",
                           "Contact support",
                           QMessageBox.Information)
        else:
            show_popup("Launch the driver first!")

    def terminate(self):
        if self.driver_status:
            self.crawler.terminate()
            self.driver_status = False
            self.status.setText("offline")
            self.status.setStyleSheet(
                "background-color: rgba(253, 4, 50, 0.8);\n"
                "border-width:4px;\n"
                "border-color:black;\n"
                "color: rgb(0, 0, 0);\n"
                "border-style:offset;\n"
                "border-radius:10px;")
        else:
            show_popup("Launch the driver first!")


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    welcome_ui = WelcomeUI(main_window)
    main_window.show()
    sys.exit(app.exec_())

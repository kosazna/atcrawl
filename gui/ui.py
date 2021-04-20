# -*- coding: utf-8 -*-

from PyQt5.QtGui import QIntValidator, QValidator
from crawlers.rellasamortiser.crawler import RellasAmortiserBrand
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.QtCore import QThreadPool

from atcrawl.gui.welcome_design import *
from atcrawl.gui.crawler_design import *
from atcrawl.crawlers import *

from atcrawl.gui.qutils import *

blue = "rgba(13, 110, 253, 0.8)"
green = "rgba(42, 214, 107, 0.8)"
teal = "rgba(32, 201, 151, 0.8)"
red = "rgba(239, 62, 79, 0.8)"
grey = "rgba(108, 117, 125, 0.8)"
yellow = "rgba(255, 193, 7, 0.8)"
cyan = "rgba(13, 202, 240, 0.8)"
orange = "rgba(253, 126, 20, 0.8)"
dark = "rgba(33, 37, 41, 0.8)"


def make_stylesheet(color, radius=5):
    _stylesheet = (f"background-color: {color};\n"
                   "border-width:4px;\n"
                   "border-color:black;\n"
                   "border-style:offset;\n"
                   f"border-radius:{radius}px;")
    return _stylesheet


def make_bt_stylesheet(color, radius=5):
    _stylesheet = (f"background-color: {color};\n"
                   "color: rgb(0, 0, 0);\n"
                   "border-width:10px;"
                   f"border-radius:{radius}px;")

    return _stylesheet


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
        self.bt_rellas.clicked.connect(
            lambda: self.init_crawler("rellasamortiser.gr"))
        self.bt_gbg.clicked.connect(
            lambda: self.init_crawler("gbg-eshop.gr"))

    def init_crawler(self, name):
        authorizer = Authorize(name)
        if authorizer.user_is_licensed():
            self.ui = CrawlerUI()
            self.ui.set_crawler(crawler_map[name]())
            self.ui.set_auth(authorizer)
            self.ui.setWindowTitle(f"atCrawl - {name}")
            self.ui.apply_masks()
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support")


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
        self.stopped = True

        self.worker = None
        self.threadpool = QThreadPool()

        self.in_folder.setText(paths.get_default_export())

        self.bt_launch.clicked.connect(self.launch)
        self.bt_terminate.clicked.connect(self.terminate)
        self.bt_collect.clicked.connect(self.start_collecting)
        self.bt_stop_collect.clicked.connect(self.stop_collecting)
        self.bt_reset.clicked.connect(self.reset)
        self.bt_export.clicked.connect(self.export)
        self.browse_folder.clicked.connect(self.folder)

    def apply_masks(self):
        if self.crawler.NAME == 'antallaktikaonline.gr':
            stylesheet = make_stylesheet(grey)
            self.in_meta1.setStyleSheet(stylesheet)
            self.in_meta1.setEnabled(False)
            self.in_meta2.setStyleSheet(stylesheet)
            self.in_meta2.setEnabled(False)
            self.in_meta3.setStyleSheet(stylesheet)
            self.in_meta3.setEnabled(False)
            self.in_meta4.setStyleSheet(stylesheet)
            self.in_meta4.setEnabled(False)
            self.meta_check.setText("")
            self.meta_check.setEnabled(False)
            self.in_model.setStyleSheet(stylesheet)
            self.in_model.setEnabled(False)

            self.label_meta0.setText("Car")

        if self.crawler.NAME == 'skroutz.gr':
            stylesheet = make_stylesheet(grey)
            self.label_meta0.setText('ID Category')
            self.label_meta1.setText('Description')
            self.label_meta2.setText('Meta Title SEO')
            self.label_meta3.setText("Meta SEO")
            self.label_meta4.setText("Extra Details")
            self.meta_check.setText("Λάδια")
            self.in_model.setStyleSheet(stylesheet)
            self.in_model.setEnabled(False)

        if self.crawler.NAME == 'rellasamortiser.gr':
            stylesheet = make_stylesheet(grey)

            self.label_meta0.setText('ID Category')
            self.label_meta1.setText('Meta Title SEO')
            self.label_meta2.setText("Meta SEO")
            self.label_meta3.setText("Skroutz")
            self.label_meta4.setText("Extra Details")
            self.meta_check.setText("")
            self.meta_check.setEnabled(False)
            self.mask_buttons('launched')
            self.change_button_status(self.bt_terminate, False, grey)

        if self.crawler.NAME == 'gbg-eshop.gr':
            stylesheet = make_stylesheet(grey)
            self.in_meta4.setStyleSheet(stylesheet)
            self.in_meta4.setEnabled(False)
            self.label_meta0.setText('ID Category')
            self.label_meta1.setText('Meta Title SEO')
            self.label_meta2.setText('Meta SEO')
            self.label_meta3.setText("Χρονολογία")
            self.meta_check.setText("")
            self.meta_check.setEnabled(False)

    def mask_output(self, text=None):
        if text is None:
            display = ''
            stylesheet = make_stylesheet(grey, radius=10)
        else:
            display = text
            stylesheet = make_stylesheet(teal, radius=10)

        self.output.setText(display)
        self.output.setStyleSheet(stylesheet)

    def change_browser_status(self, status):
        if status == 'online':
            stylesheet = make_stylesheet(green, radius=10)
        else:
            stylesheet = make_stylesheet(red, radius=10)

        self.status_browser.setText(status)
        self.status_browser.setStyleSheet(stylesheet)

    def change_crawler_status(self, status):
        if status == 'running':
            stylesheet = make_stylesheet(green, radius=10)
        elif status == 'offline':
            stylesheet = make_stylesheet(red, radius=10)
        else:
            stylesheet = make_stylesheet(yellow, radius=10)

        self.status_crawler.setText(status)
        self.status_crawler.setStyleSheet(stylesheet)

    def change_button_status(self, button, status, color):
        button.setEnabled(status)
        button.setStyleSheet(make_bt_stylesheet(color))

    def count_parsed(self):
        try:
            self.nitems = self.crawler.data.shape[0]
        except AttributeError:
            self.nitems = self.crawler.transformed_data.shape[0]
        return str(self.nitems)

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

    def get_model(self):
        return self.in_model.text()

    def get_params(self):
        _params = {'meta0': self.in_meta0.text(),
                   'meta1': self.in_meta1.text(),
                   'meta2': self.in_meta2.text(),
                   'meta3': self.in_meta3.text(),
                   'meta4': self.in_meta4.text(),
                   'meta_check': self.meta_check.isChecked(),
                   'brand': self.get_brand(),
                   'discount': self.get_discount(),
                   'model': self.get_model()}

        return _params

    def mask_buttons(self, process):
        if self.crawler.NAME != 'rellasamortiser.gr':
            if process == 'launched':
                self.change_button_status(self.bt_launch, False, grey)
                self.change_button_status(self.bt_collect, True, green)
                self.change_button_status(self.bt_stop_collect, False, grey)
                self.change_button_status(self.bt_reset, True, yellow)
                self.change_button_status(self.bt_terminate, True, blue)
                self.change_button_status(self.bt_export, False, grey)
            elif process == 'collecting':
                self.change_button_status(self.bt_launch, False, grey)
                self.change_button_status(self.bt_collect, False, grey)
                self.change_button_status(self.bt_stop_collect, True, red)
                self.change_button_status(self.bt_reset, False, grey)
                self.change_button_status(self.bt_terminate, False, grey)
                self.change_button_status(self.bt_export, False, grey)
            elif process == 'done_collecting':
                self.change_button_status(self.bt_launch, False, grey)
                self.change_button_status(self.bt_collect, False, grey)
                self.change_button_status(self.bt_stop_collect, False, grey)
                self.change_button_status(self.bt_reset, True, yellow)
                self.change_button_status(self.bt_terminate, True, blue)
                self.change_button_status(self.bt_export, True, cyan)
            else:
                self.change_button_status(self.bt_launch, True, blue)
                self.change_button_status(self.bt_collect, False, grey)
                self.change_button_status(self.bt_stop_collect, False, grey)
                self.change_button_status(self.bt_reset, False, grey)
                self.change_button_status(self.bt_terminate, False, grey)
                self.change_button_status(self.bt_export, False, grey)
        else:
            if process == 'launched':
                self.change_button_status(self.bt_launch, False, grey)
                self.change_button_status(self.bt_collect, True, green)
                self.change_button_status(self.bt_stop_collect, False, grey)
                self.change_button_status(self.bt_export, False, grey)
                self.change_button_status(self.bt_reset, False, grey)
            elif process == 'collecting':
                self.change_button_status(self.bt_launch, False, grey)
                self.change_button_status(self.bt_collect, False, grey)
                self.change_button_status(self.bt_stop_collect, True, red)
                self.change_button_status(self.bt_export, False, grey)
                self.change_button_status(self.bt_reset, False, grey)
            elif process == 'done_collecting':
                self.change_button_status(self.bt_launch, False, grey)
                self.change_button_status(self.bt_collect, True, green)
                self.change_button_status(self.bt_stop_collect, False, grey)
                self.change_button_status(self.bt_export, True, cyan)
                self.change_button_status(self.bt_reset, True, yellow)

    def launch(self):
        self.url = self.in_url.text()
        self.old_url = self.in_url.text()

        if self.url is not None and self.url != '':
            self.crawler.set_url(self.url)
            self.crawler.launch('Firefox', paths.get_firefox())
            self.driver_status = True

            self.change_browser_status("online")
            self.change_crawler_status('idle')

            self.mask_buttons('launched')
        else:
            show_popup("URL is not set. Launch cancelled!",
                       "Set the url and then launch.",
                       QMessageBox.Critical)

    def collect(self, progress_callback):
        if self.crawler.NAME != 'rellasamortiser.gr':
            npage = 1
            self.crawler.pre_collect()
            progress_callback.emit(f"Collecting page {npage}")
            while not self.stopped and self.crawler.click('Next'):

                if self.crawler.NAME == 'gbg-eshop.gr':
                    _str = f"Collecting page {npage} of {self.crawler.nitems}"
                    npage += 1
                else:
                    npage += 1
                    _str = f"Collecting page {npage}"

                progress_callback.emit(_str)
                self.crawler.collect(gather='single')
            progress_callback.emit(f"Pages Finished")
        else:
            self.crawler.set_url(self.in_url.text())
            progress_callback.emit("Finding URLs...")
            self.crawler.pre_collect()

            npage = 1

            while not self.stopped and self.crawler.next_url():
                current = f"Collecting -> {self.crawler.current_url}"
                total = f"URL {npage}/{self.crawler.total_urls}"
                progress_callback.emit(f"{total} | {current}")
                self.crawler.collect(gather='single')
                npage += 1

    def start_collecting(self):
        self.stopped = False
        self.change_crawler_status('running')
        self.mask_output()
        self.mask_buttons('collecting')

        if self.crawler.NAME == "antallaktikaonline.gr":
            self.crawler.first_run = False

        if self.crawler.NAME == "rellasamortiser.gr":
            self.count_items.setText("0")

        self.run_threaded_process(self.collect,
                                  self.collecting_updates,
                                  self.finished_collecting)

    def collecting_updates(self, text):
        self.mask_output(text)

    def finished_collecting(self):
        self.stopped = True

        if self.crawler.NAME == "antallaktikaonline.gr":
            self.crawler.parse()

        self.mask_buttons('done_collecting')

        self.change_crawler_status('idle')
        self.to_export = True
        if self.check_export.isChecked():
            self.export()

    def stop_collecting(self):
        self.stopped = True
        return

    def run_threaded_process(self, process, on_update, on_complete):
        worker = Worker(process)
        worker.signals.finished.connect(on_complete)
        worker.signals.progress.connect(on_update)
        self.threadpool.start(worker)

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

                self.count_items.setText(self.count_parsed())

                _pre = "Generated file --> "
                _output = _folder + '\\' + _name + f'.{_type}'
                self.mask_output(_pre + _output)

                self.to_export = False
            else:
                show_popup("You are not authorized",
                           "Contact support",
                           QMessageBox.Information)
        else:
            show_popup("Nothing to export")

    def reset(self):
        if self.crawler.NAME == 'rellasamortiser.gr':
            self.crawler.reset(self.in_url.text())
            self.count_items.setText('0')
            self.mask_buttons('launched')
            self.mask_output()
        else:
            if self.driver_status:
                _url = self.in_url.text()

                if _url == self.old_url:
                    self.crawler.reset()
                else:
                    self.crawler.reset(_url)
                    self.old_url = _url

                self.threadpool.clear()
                self.to_export = False

                self.mask_output()
                self.mask_buttons('launched')
                self.count_items.setText('0')
            else:
                show_popup("Launch the driver first!")

    def terminate(self):
        if self.driver_status:
            self.crawler.terminate()
            self.driver_status = False
            self.change_browser_status("offline")
            self.change_crawler_status("offline")
            self.mask_buttons('terminated')
        else:
            show_popup("Launch the driver first!")


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    welcome_ui = WelcomeUI(main_window)
    main_window.show()
    sys.exit(app.exec_())

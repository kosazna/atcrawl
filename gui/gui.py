# -*- coding: utf-8 -*-

from atcrawl.crawlers import *
from atcrawl.gui.edit import EditWindow
from atcrawl.gui.welcome_design import *
from atcrawl.gui.widgets import *
from atcrawl.gui.worker import Worker
from PyQt5.QtCore import QThreadPool


class WelcomeUI(Ui_WelcomeUI):
    def __init__(self, window):
        self.setupUi(window)
        self.ui = None

        self.bt_antallaktika.clicked.connect(
            lambda: self.init_crawler("antallaktikaonline.gr"))
        self.bt_skroutz.clicked.connect(
            lambda: self.init_crawler("skroutz.gr"))
        self.bt_rellas.clicked.connect(
            lambda: self.init_crawler("rellasamortiser.gr"))
        self.bt_gbg.clicked.connect(
            lambda: self.init_crawler("gbg-eshop.gr"))
        self.bt_edit.clicked.connect(self.init_tools)

    def init_crawler(self, name):
        if authorizer.user_is_licensed(name):
            self.ui = CrawlerUI()
            self.ui.set_crawler(crawler_map[name]())
            self.ui.set_auth(authorizer)
            self.ui.setWindowTitle(f"atCrawl Services - {name}")
            self.ui.apply_masks()
            self.ui.show()
        else:
            show_popup("You are not authorized",
                       "Contact support")

    def init_tools(self):
        self.ui = EditWindow()
        self.ui.show()


class CrawlerUI(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(CrawlerUI, self).__init__(parent=parent, *args, **kwargs)
        self.setupUi()

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
        self.output = None

        self.worker = None
        self.threadpool = QThreadPool()

        self.statusGeneral.subscribe(self.open_file)
        self.outputFolder.setText(paths.get_default_export())

        self.buttonLaunch.clicked.connect(self.launch)
        self.buttonTerminate.clicked.connect(self.terminate)
        self.buttonCollect.clicked.connect(self.start_collecting)
        self.buttonStop.clicked.connect(self.stop_collecting)
        self.buttonReset.clicked.connect(self.reset)

    def setupUi(self):
        self.setObjectName("MainWidget")
        self.setStyleSheet(cssGuide)
        self.setWindowTitle("atCrawl Services")
        self.resize(500, 350)
        self.buttonLaunch = Button('launch')
        self.buttonCollect = Button('collect')
        self.buttonStop = Button('stop')
        self.buttonReset = Button('reset')
        self.buttonTerminate = Button('terminate')
        self.checkMeta = CheckInput('MetaCheck')
        self.inputUrl = InputParameter('URL')
        self.inputMeta0 = InputParameter('Meta0', size=('Small', 'Small'))
        self.inputMeta1 = InputParameter('Meta1', size=('Small', 'Small'))
        self.inputMeta2 = InputParameter('Meta2', size=('Small', 'Small'))
        self.inputMeta3 = IntInputParameter('Meta3', value_range=(-99, 99), size=('Small', 'Small'))
        self.inputMeta4 = InputParameter('Meta4', size=('Big', 'Big'))
        self.inputMeta5 = InputParameter('Meta5', size=('Big', 'Big'))
        self.inputMeta6 = InputParameter('Meta6', size=('Big', 'Big'))
        self.inputMeta7 = InputParameter('Meta7', size=('Big', 'Big'))
        self.inputFilename = FileNameInput('Filename', size=('Small', 'Small'))
        self.outputFolder = FolderInput('Folder', size='Big')
        self.statusBrowser = StatusIndicator('Browser', 'offline')
        self.statusCrawler = StatusIndicator('Crawler', 'offline')
        self.statusGeneral = StatusIndicator()
        self.layoutGui = QHBoxLayout()
        self.layoutLeft = QVBoxLayout()
        self.layoutTop = QHBoxLayout()
        self.layoutParams = QHBoxLayout()
        self.layoutSmall = QVBoxLayout()
        self.layoutBig = QVBoxLayout()
        self.layoutBottom = QVBoxLayout()
        self.layoutButtons = QVBoxLayout()
        self.layoutStatus = QHBoxLayout()
        self.layoutTop.addWidget(self.inputUrl)
        self.layoutSmall.addWidget(self.inputMeta0, 0, Qt.AlignLeft)
        self.layoutSmall.addWidget(self.inputMeta1, 0, Qt.AlignLeft)
        self.layoutSmall.addWidget(self.inputMeta2, 0, Qt.AlignLeft)
        self.layoutSmall.addWidget(self.inputMeta3, 0, Qt.AlignLeft)
        self.layoutSmall.addStretch()
        self.layoutSmall.addWidget(self.inputFilename, 0, Qt.AlignLeft)
        self.layoutBig.addWidget(self.inputMeta4)
        self.layoutBig.addWidget(self.inputMeta5)
        self.layoutBig.addWidget(self.inputMeta6)
        self.layoutBig.addWidget(self.inputMeta7)
        self.layoutBig.addStretch()
        self.layoutBig.addWidget(self.outputFolder)
        self.layoutButtons.addWidget(self.checkMeta)
        self.layoutButtons.addWidget(self.buttonLaunch)
        self.layoutButtons.addWidget(self.buttonCollect)
        self.layoutButtons.addWidget(self.buttonStop)
        self.layoutButtons.addWidget(self.buttonReset)
        self.layoutButtons.addWidget(self.buttonTerminate)
        self.layoutStatus.addWidget(self.statusBrowser)
        self.layoutStatus.addWidget(self.statusCrawler)
        self.layoutStatus.addStretch()
        self.layoutStatus.addWidget(self.statusGeneral, 1)
        self.layoutParams.addLayout(self.layoutSmall)
        self.layoutParams.addLayout(self.layoutBig)
        self.layoutBottom.addLayout(self.layoutStatus)
        self.layoutLeft.addLayout(self.layoutTop)
        self.layoutLeft.addLayout(self.layoutParams)
        self.layoutLeft.addLayout(self.layoutBottom)
        self.layoutGui.addLayout(self.layoutLeft)
        self.layoutGui.addLayout(self.layoutButtons)
        self.setLayout(self.layoutGui)

    def open_file(self):
        if self.output is not None:
            os.startfile(self.output)

    def set_crawler(self, crawler_obj):
        self.crawler = crawler_obj

    def set_auth(self, authorizer):
        self.auth = authorizer

    def apply_masks(self):
        if self.crawler.NAME == 'antallaktikaonline.gr':
            self.inputMeta0.setLabel("Brand")
            self.inputMeta1.setLabel("Car")
            self.inputMeta2.hide()
            self.inputMeta3.setLabel("Price (%)")
            self.inputMeta4.hide()
            self.inputMeta5.hide()
            self.inputMeta6.hide()
            self.inputMeta7.hide()
            self.checkMeta.hide()
            self.mask_buttons('start')
            self.inputMeta0.setCompleter(MANUFACTURES_BRANDS)

        if self.crawler.NAME == 'skroutz.gr':
            self.inputMeta0.setLabel("Brand")
            self.inputMeta1.hide()
            self.inputMeta2.setLabel("ID Cat.")
            self.inputMeta3.setLabel("Price (%)")
            self.inputMeta4.setLabel("Description")
            self.inputMeta5.setLabel("Meta Title SEO")
            self.inputMeta6.setLabel("Meta SEO")
            self.inputMeta7.setLabel("Extra Details")
            self.checkMeta.setText("Λάδια")
            self.checkMeta.toggle()
            self.mask_buttons('start')
            self.inputMeta0.setCompleter(MANUFACTURES_BRANDS)

        if self.crawler.NAME == 'rellasamortiser.gr':
            self.inputMeta0.setLabel("Brand")
            self.inputMeta1.setLabel("Model")
            self.inputMeta2.setLabel("ID Cat.")
            self.inputMeta3.setLabel("Price (%)")
            self.inputMeta4.setLabel("Skroutz")
            self.inputMeta5.setLabel("Meta Title SEO")
            self.inputMeta6.setLabel("Meta SEO")
            self.inputMeta7.setLabel("Extra Details")
            self.checkMeta.hide()
            self.mask_buttons('launched')
            self.inputMeta0.setCompleter(CAR_BRANDS)

        if self.crawler.NAME == 'gbg-eshop.gr':
            self.inputMeta0.setLabel("Brand")
            self.inputMeta1.setLabel("Model")
            self.inputMeta2.setLabel("ID Cat.")
            self.inputMeta3.setLabel("Price (%)")
            self.inputMeta4.setLabel("Χρονολογία")
            self.inputMeta5.setLabel("Meta Title SEO")
            self.inputMeta6.setLabel("Meta SEO")
            self.inputMeta7.hide()
            self.checkMeta.hide()
            self.mask_buttons('start')
            self.inputMeta0.setCompleter(CAR_BRANDS)

    def mask_output(self, text=None):
        if text is None:
            self.statusGeneral.disable()
        else:
            self.statusGeneral.enable(text)

    def change_browser_status(self, status):
        if status == 'online':
            self.statusBrowser.disable(status)
        else:
            self.statusBrowser.disable(status)

    def change_crawler_status(self, status):
        if status == 'running':
            self.statusCrawler.disable(status)
        elif status == 'offline':
            self.statusCrawler.disable(status)
        else:
            self.statusCrawler.disable(status)

    def count_parsed(self):
        try:
            self.nitems = self.crawler.data.shape[0]
        except AttributeError:
            self.nitems = self.crawler.transformed_data.shape[0]
        return str(self.nitems)

    def get_folder(self):
        _folder = self.outputFolder.getText()

        if _folder == '':
            self.folder_name = paths.get_cwd()
        else:
            self.folder_name = _folder

        return self.folder_name

    def get_filename(self):
        _filename = self.inputFilename.getText()
        if _filename == '':
            self.file_name = 'Collected_Data'
        else:
            self.file_name = _filename

        return self.file_name

    def get_params(self):
        _params = {'meta0': self.inputMeta0.getText(),
                   'meta1': self.inputMeta1.getText(),
                   'meta2': self.inputMeta2.getText(),
                   'meta3': self.inputMeta3.getText(),
                   'meta4': self.inputMeta4.getText(),
                   'meta5': self.inputMeta5.getText(),
                   'meta6': self.inputMeta6.getText(),
                   'meta7': self.inputMeta7.getText(),
                   'meta_check': self.checkMeta.isChecked()}

        return _params

    def mask_buttons(self, process):
        if self.crawler.NAME != 'rellasamortiser.gr':
            if process == 'launched':
                self.buttonLaunch.disable()
                self.buttonCollect.enable(green)
                self.buttonStop.disable()
                self.buttonReset.enable(yellow)
                self.buttonTerminate.enable(blue)
            elif process == 'collecting':
                self.buttonLaunch.disable()
                self.buttonCollect.disable()
                self.buttonStop.enable(red)
                self.buttonReset.disable()
                self.buttonTerminate.disable()
            elif process == 'done_collecting':
                self.buttonLaunch.disable()
                self.buttonCollect.disable()
                self.buttonStop.disable()
                self.buttonReset.enable(yellow)
                self.buttonTerminate.enable(blue)
            else:
                self.buttonLaunch.enable(blue)
                self.buttonCollect.disable()
                self.buttonStop.disable()
                self.buttonReset.disable()
                self.buttonTerminate.disable()
        else:
            if process == 'launched':
                self.buttonLaunch.disable()
                self.buttonCollect.enable(green)
                self.buttonStop.disable()
                self.buttonReset.disable()
                self.buttonTerminate.disable()
            elif process == 'collecting':
                self.buttonLaunch.disable()
                self.buttonCollect.disable()
                self.buttonStop.enable(red)
                self.buttonReset.disable()
                self.buttonTerminate.disable()
            elif process == 'done_collecting':
                self.buttonLaunch.disable()
                self.buttonCollect.enable(green)
                self.buttonStop.disable()
                self.buttonReset.enable(yellow)
                self.buttonTerminate.disable()

    def launch(self):
        self.url = self.inputUrl.getText()
        self.old_url = self.inputUrl.getText()

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
            self.crawler.set_url(self.inputUrl.getText())
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
            if self.auth.user_is_licensed(self.crawler.NAME):
                _name = self.get_filename()
                _folder = self.get_folder()
                _type = 'xlsx'

                self.crawler.transform(**self.get_params())

                self.crawler.export(name=_name,
                                    folder=_folder,
                                    export_type=_type)

                items = self.count_parsed()
                _output = _folder + f'/{_name}.{_type}'
                self.output = _output
                self.mask_output(f"Items: {items} | {_output}")

                self.to_export = False
            else:
                show_popup("You are not authorized",
                           "Contact support",
                           QMessageBox.Information)
        else:
            show_popup("Nothing to export")

    def reset(self):
        if self.crawler.NAME == 'rellasamortiser.gr':
            self.crawler.reset(self.inputUrl.getText())
            self.mask_buttons('launched')
            self.mask_output()
        else:
            if self.driver_status:
                _url = self.inputUrl.getText()

                if _url == self.old_url:
                    self.crawler.reset()
                else:
                    self.crawler.reset(_url)
                    self.old_url = _url

                self.threadpool.clear()
                self.to_export = False

                self.mask_output()
                self.mask_buttons('launched')
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
    screen = app.screens()[0]
    dpi = screen.physicalDotsPerInch()
    main_window = QtWidgets.QMainWindow()
    welcome_ui = WelcomeUI(main_window)
    main_window.show()
    sys.exit(app.exec_())

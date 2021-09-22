# -*- coding: utf-8 -*-

from atcrawl.crawlers import *
from atcrawl.core.engine import *
from atcrawl.utilities.auth import *
from atcrawl.utilities.paths import *
from atcrawl.gui.edit import EditWindow
from atcrawl.gui.welcome_design import *
from atcrawl.gui.widgets import *
from atcrawl.gui.worker import Worker, WorkerSignalsStr
from PyQt5.QtCore import QThreadPool


class TransformUI(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(TransformUI, self).__init__(parent=parent, *args, **kwargs)
        self.setupUi()

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

        # self.buttonLaunch = Button('launch')
        # self.buttonCollect = Button('collect')
        # self.buttonStop = Button('stop')
        # self.buttonReset = Button('reset')
        # self.buttonTerminate = Button('terminate')

        self.buttonTransform = Button('transform')


        self.checkMeta = CheckInput('MetaCheck')
        self.inputUrl = InputParameter('URL')
        self.inputMeta0 = InputParameter('Meta0', size=(70, 200))
        self.inputMeta1 = InputParameter('Meta1', size=(70, 200))
        self.inputMeta2 = InputParameter('Meta2', size=(70, 200))
        self.inputMeta3 = IntInputParameter(
            'Meta3', value_range=(-99, 99), size=(70, 200))
        self.inputMeta4 = InputParameter('Meta4', size=(100, 400))
        self.inputMeta5 = InputParameter('Meta5', size=(100, 400))
        self.inputMeta6 = InputParameter('Meta6', size=(100, 400))
        self.inputMeta7 = InputParameter('Meta7', size=(100, 400))
        self.inputFilename = FileNameInput('Filename', size=(70, 200))
        self.outputFolder = FolderInput('Folder', size=100)

        # self.statusBrowser = StatusIndicator('Browser', 'offline')
        # self.statusCrawler = StatusIndicator('Crawler', 'offline')
        # self.statusGeneral = StatusIndicator()

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

    def load(self):
        pass

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
            # self.mask_buttons('launched')
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
            # self.mask_buttons('start')
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
            # self.mask_buttons('launched')
            self.inputMeta0.setCompleter(CAR_BRANDS)

        if self.crawler.NAME == 'gbg-eshop.gr':
            self.inputMeta0.setLabel("Brand")
            self.inputMeta1.setLabel("Model")
            self.inputMeta2.setLabel("ID Cat.")
            self.inputMeta3.setLabel("Price (%)")
            self.inputMeta4.setLabel("Πρόθεμα")
            self.inputMeta5.setLabel("Χρονολογία")
            self.inputMeta6.setLabel("Meta Title SEO")
            self.inputMeta7.setLabel("Meta SEO")

            self.checkMeta.hide()
            # self.mask_buttons('start')
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
        if self.crawler.NAME in ['skroutz.gr',
                                 'gbg-eshop.gr']:
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
        elif self.crawler.NAME in ['antallaktikaonline.gr',
                                   'rellasamortiser.gr']:
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

    def export(self):
        if self.to_export:
            if self.auth.user_is_licensed(self.crawler.NAME):
                _name = self.get_filename()
                _folder = self.get_folder()
                _type = 'xlsx'
                _output = _folder + f'/{_name}.{_type}'
                _params = self.get_params()

                if self.crawler.NAME in ['antallaktikaonline.gr',
                                         'rellasamortiser.gr']:
                    self.crawler.drop_n_sort()
                    self.crawler.backup2db(str(_params))

                self.crawler.transform(**_params)

                self.crawler.export(name=_name,
                                    folder=_folder,
                                    export_type=_type)

                if self.crawler.NAME in ['antallaktikaonline.gr',
                                         'rellasamortiser.gr']:
                    job_id = self.crawler.sql.get_last_jobid()
                    self.crawler.sql.update_output(job_id, _output)

                items = self.count_parsed()
                self.output = _output
                self.mask_output(f"Items: {items} | {_output}")

                self.to_export = False
            else:
                show_popup("You are not authorized",
                           "Contact support",
                           QMessageBox.Information)
        else:
            show_popup("Nothing to export")


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    screen = app.screens()[0]
    dpi = screen.physicalDotsPerInch()
    main_window = QtWidgets.QMainWindow()
    welcome_ui = WelcomeUI(main_window)
    main_window.show()
    sys.exit(app.exec_())

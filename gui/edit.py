# -*- coding: utf-8 -*-

from atcrawl.gui.widgets import *
from atcrawl.gui.worker import Worker, WorkerSignalsTuple
from atcrawl.utilities.auth import *
from atcrawl.utilities.funcs import *
from atcrawl.utilities.paths import *
from PyQt5.QtCore import QThreadPool

cwd = paths.get_base_folder()


class MainEdit(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.threadpool = QThreadPool()
        self.no_validate = ()
        self.can_process = False
        self.last_status = None
        self.output = None

    def open_file(self):
        if self.output is not None:
            os.startfile(self.output)

    def mask_output(self, text=None):
        if text is None:
            self.status.disable()
        else:
            self.status.enable(text)

    def assert_process_capabilities(self):
        bools = []
        for key, value in self.getParams().items():
            if key in self.no_validate:
                continue
            if value:
                bools.append(True)
            else:
                bools.append(False)

        self.can_process = all(bools)

    def run_threaded_process(self, process, on_update, on_finish):
        worker = Worker(process, WorkerSignalsTuple)
        worker.signals.finished.connect(on_finish)
        worker.signals.progress.connect(on_update)
        worker.signals.popup.connect(show_popup)
        self.threadpool.start(worker)

    def start_process(self):
        self.run_threaded_process(self.execute,
                                  self.process_updates,
                                  self.end_process)

    def process_updates(self, values):
        self.progressBar.setValueMaximum(values[0], values[1])
        try:
            if values[2] is not None:
                self.mask_output(values[2])
                self.last_status = values[2]
        except IndexError:
            pass

    def end_process(self):
        if self.can_process:
            self.progressBar.setValue(self.progressBar.maximum())
            self.progressBar.setStyle("ProgressBarFinished")

        if self.last_status is not None:
            if os.path.exists(self.last_status):
                self.status.enable(self.last_status)
                self.output = self.last_status

    def getParams(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):
        pass


class SplitFileEdit(MainEdit):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.button.subscribe(self.start_process)
        self.status.subscribe(self.open_file)
        self.can_process = False

    def setupUi(self):
        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL,
                                      )
        self.destination = FolderInput("Αποθήκευση αρχέιων στον φάκελο:",
                                       orientation=VERTICAL,
                                       )
        self.splitRatio = IntInputParameter("Σπάσιμο αρχείου ανά:",
                                            orientation=VERTICAL)

        self.progressBar = ProgressBar()

        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator()
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.progressBar)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addWidget(self.splitRatio)
        self.pageLayout.addStretch()
        self.pageLayout.addWidget(self.status)
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def getParams(self):
        _params = {'filepath': self.fileToModify.getText(),
                   'destination': self.destination.getText(),
                   'k': int(self.splitRatio.getText())}

        return _params

    def execute(self, progress_callback, progress_popup):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed('split_file'):
            if self.can_process:
                params = self.getParams()
                split_file(**params, progress_callback=progress_callback)
            else:
                progress_popup.emit("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            progress_popup.emit("You are not authorized",
                                "Contact support")


class DownloadImagesEdit(MainEdit):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.fileToModify.lineEdit.textChanged.connect(self.clearCombos)
        self.button.subscribe(self.start_process)
        self.status.subscribe(self.open_file)
        self.can_process = False

    def setupUi(self):
        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.fileToModify.setBrowseCallback(self.readInputFile)
        self.combosLayout = QHBoxLayout()
        self.colCombo1 = ComboInput("Όνομα εικόνας", size=(150, 150))
        self.colCombo2 = ComboInput("URL εικόνας", size=(150, 150))
        self.combosLayout.addWidget(self.colCombo1)
        self.combosLayout.addWidget(self.colCombo2)
        self.prefix = InputParameter("Link μπροστά από το όνομα της εικόνας:",
                                     orientation=VERTICAL)
        self.destination = FolderInput("Αποθήκευση αρχέιων στον φάκελο:",
                                       orientation=VERTICAL)

        self.progressBar = ProgressBar()

        self.destination.setText(paths.get_images_export())
        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.progressBar)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addLayout(self.combosLayout)
        self.pageLayout.addWidget(self.prefix)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addStretch()
        self.pageLayout.addWidget(self.status)
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def getParams(self):
        _params = {'src': self.fileToModify.getText(),
                   'img_name': self.colCombo1.getCurrentText(),
                   'img_url': self.colCombo2.getCurrentText(),
                   'prefix': self.prefix.getText(),
                   'dst': self.destination.getText()}

        return _params

    def readInputFile(self):
        _file = self.fileToModify.getText()
        if os.path.exists(_file):
            _file_ext = os.path.splitext(_file)[1]
            if _file_ext in ['.xlsx', '.xls']:
                _df = pd.read_excel(_file)
                _cols = _df.columns.tolist()

                self.colCombo1.addItems(_cols)
                self.colCombo2.addItems(_cols)

    def clearCombos(self):
        self.colCombo1.clearItems()
        self.colCombo2.clearItems()

    def execute(self, progress_callback, progress_popup):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("img_downloader"):
            if self.can_process:
                params = self.getParams()
                src = params.get('src')
                url_col = params.get('img_url')
                name_col = params.get('img_name')
                prefix = params.get('prefix')
                dst = params.get('dst')

                df = pd.read_excel(src, dtype='string')

                url_list = df[url_col].copy()
                name_list = df[name_col].copy()

                if prefix.endswith('/'):
                    _prefix = prefix[:-1]
                else:
                    _prefix = prefix

                new_names = f"{_prefix}/" + df[name_col] + '.jpg'

                download_images(url_list,
                                dst,
                                name_list,
                                progress_callback=progress_callback)
                df[url_col] = new_names
                df.to_excel(src, index=False)
                progress_callback.emit((100, 100, src))
            else:
                progress_popup.emit("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            progress_popup.emit("You are not authorized",
                                "Contact support")


class CreateImagesEdit(MainEdit):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.button.subscribe(self.start_process)
        self.status.subscribe(self.open_file)
        self.can_process = False
        self.no_validate = ('prefix_images')

    def setupUi(self):
        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.source = FolderInput("Φάκελος πρωτότυπων εικόνων:",
                                  orientation=VERTICAL)
        self.destination = FolderInput("Αποθήκευση αρχέιων στον φάκελο:",
                                       orientation=VERTICAL)
        self.prefix = InputParameter("Link μπροστά από το όνομα της εικόνας:",
                                     orientation=VERTICAL)

        self.progressBar = ProgressBar()

        self.source.setText(paths.get_images_import())
        self.destination.setText(paths.get_images_export())
        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.progressBar)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addWidget(self.source)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addWidget(self.prefix)
        self.pageLayout.addStretch()
        self.pageLayout.addWidget(self.status)
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def getParams(self):
        _params = {'data': self.fileToModify.getText(),
                   'src_images': self.source.getText(),
                   'dst_images': self.destination.getText(),
                   'prefix_images': self.prefix.getText()}

        return _params

    def execute(self, progress_callback, progress_popup):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("create_images"):
            if self.can_process:
                params = self.getParams()
                create_images(**params, progress_callback=progress_callback)
            else:
                progress_popup.emit("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            progress_popup.emit("You are not authorized",
                                "Contact support")


class MergeEdit(MainEdit):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.button.subscribe(self.start_process)
        self.status.subscribe(self.open_file)
        self.can_process = False
        self.no_validate = ('col1', 'val1')

    def setupUi(self):
        self.source = FolderInput("Φάκελος αρχείων:",
                                  orientation=VERTICAL)
        self.colsLayout1 = QVBoxLayout()
        self.newColName1 = InputParameter("Νέα στήλη 1", size=(150, 100))

        self.newColName1.setPlaceholder("Προαιρετικό")
        self.newColValue1 = InputParameter(
            "Τιμή στήλης 1", size=(150, 100))

        self.newColValue1.setPlaceholder("Προαιρετικό")
        self.colsLayout1.addWidget(self.newColName1)
        self.colsLayout1.addWidget(self.newColValue1)
        self.destination = FileOutput("Αποθήκευση αρχείου:",
                                      orientation=VERTICAL)

        self.progressBar = ProgressBar()

        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.progressBar)
        self.buttonLayout.addWidget(self.button)
        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.source)
        self.pageLayout.addLayout(self.colsLayout1)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addStretch()
        self.pageLayout.addWidget(self.status)
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def getParams(self):
        _params = {'src': self.source.getText(),
                   'col1': self.newColName1.getText(),
                   'val1': self.newColValue1.getText(),
                   'dst': self.destination.getText()}

        return _params

    def execute(self, progress_callback, progress_popup):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("create_images"):
            if self.can_process:
                params = self.getParams()
                merge_file(**params, progress_callback=progress_callback)
            else:
                progress_popup.emit("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            progress_popup.emit("You are not authorized",
                                "Contact support")


class FilterEdit(MainEdit):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.fileToModify.lineEdit.textChanged.connect(self.clearCombos)
        self.button.subscribe(self.start_process)
        self.status.subscribe(self.open_file)
        self.can_process = False

    def setupUi(self):
        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.fileToModify.setBrowseCallback(self.readInputFile)
        self.horLayout = QHBoxLayout()
        self.combosLayout = QVBoxLayout()
        self.colCombo1 = ComboInput("Στήλη εφαρμογής", size=(150, 150))
        self.colCombo2 = ComboInput("Στήλη αλλαγών", size=(150, 150))
        self.combosLayout.addWidget(self.colCombo1)
        self.combosLayout.addWidget(self.colCombo2)
        self.paramsLayout = QVBoxLayout()
        self.paramFilter = InputParameter("Φίλτρο:", size=(150, 100))
        self.paramTrue = InputParameter(
            "Τιμή για θετικές:", size=(150, 100))
        self.paramFalse = InputParameter(
            "Τιμή για αρνητικές:", size=(150, 100))

        self.progressBar = ProgressBar()

        self.paramsLayout.addWidget(self.paramFilter)
        self.paramsLayout.addWidget(self.paramTrue)
        self.paramsLayout.addWidget(self.paramFalse)
        self.horLayout.addLayout(self.combosLayout)
        self.horLayout.addLayout(self.paramsLayout)
        self.destination = FileOutput("Αποθήκευση αρχείου:",
                                      orientation=VERTICAL)
        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.progressBar)
        self.buttonLayout.addWidget(self.button)
        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addLayout(self.horLayout)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addStretch()
        self.pageLayout.addWidget(self.status)
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def getParams(self):
        self.assert_process_capabilities()
        _params = {'src': self.fileToModify.getText(),
                   'col1': self.colCombo1.getCurrentText(),
                   'col2': self.colCombo2.getCurrentText(),
                   'pattern': self.paramFilter.getText(),
                   'val_true': self.paramTrue.getText(),
                   'val_false': self.paramFalse.getText(),
                   'dst': self.destination.getText()}

        return _params

    def readInputFile(self):
        _file = self.fileToModify.getText()
        if os.path.exists(_file):
            _file_ext = os.path.splitext(_file)[1]
            if _file_ext in ['.xlsx', '.xls']:
                _df = pd.read_excel(_file)
                _cols = _df.columns.tolist()

                self.colCombo1.addItems(_cols)
                self.colCombo2.addItems(_cols)

    def clearCombos(self):
        self.colCombo1.clearItems()
        self.colCombo2.clearItems()

    def execute(self, progress_callback, progress_popup):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("filter_run"):
            if self.can_process:
                params = self.getParams()
                filter_file(**params, progress_callback=progress_callback)
            else:
                progress_popup.emit("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            progress_popup.emit("You are not authorized",
                                "Contact support")


class SortEdit(MainEdit):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.fileToModify.lineEdit.textChanged.connect(self.clearCombos)
        self.button.subscribe(self.start_process)
        self.status.subscribe(self.open_file)
        self.can_process = False

    def setupUi(self):
        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.fileToModify.setBrowseCallback(self.readInputFile)
        self.colCombo1 = ComboInput("Στήλη εφαρμογής", size=(150, 150))

        self.destination = FileOutput("Αποθήκευση αρχείου:",
                                      orientation=VERTICAL)

        self.progressBar = ProgressBar()

        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.progressBar)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addWidget(self.colCombo1)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addStretch()
        self.pageLayout.addWidget(self.status)
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def getParams(self):
        _params = {'src': self.fileToModify.getText(),
                   'col': self.colCombo1.getCurrentText(),
                   'dst': self.destination.getText()}

        return _params

    def readInputFile(self):
        _file = self.fileToModify.getText()
        if os.path.exists(_file):
            _file_ext = os.path.splitext(_file)[1]
            if _file_ext in ['.xlsx', '.xls']:
                _df = pd.read_excel(_file)
                _cols = _df.columns.tolist()

                self.colCombo1.addItems(_cols)

    def clearCombos(self):
        self.colCombo1.clearItems()

    def execute(self, progress_callback, progress_popup):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("sort_run"):
            if self.can_process:
                params = self.getParams()
                sort_file(**params, progress_callback=progress_callback)
            else:
                progress_popup.emit("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            progress_popup.emit("You are not authorized",
                                "Contact support")


class ReplaceWordsEdit(MainEdit):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.button.subscribe(self.start_process)
        self.status.subscribe(self.open_file)
        self.can_process = False

    def setupUi(self):
        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.replacements = FileInput("Αρχείο με τις αντικαταστάσεις:",
                                      orientation=VERTICAL)
        self.destination = FileOutput("Αποθήκευση επεξεργασμένου αρχείου:",
                                      orientation=VERTICAL)

        self.columns = InputParameter("Στήλες (διαχωρισμένες με παύλα [-])",
                                      orientation=VERTICAL)

        self.progressBar = ProgressBar()

        self.replacements.setText(paths.get_replacements())
        self.columns.setText("title-meta_title_seo-meta_seo-details")
        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.progressBar)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addWidget(self.replacements)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addWidget(self.columns)
        self.pageLayout.addStretch()
        self.pageLayout.addWidget(self.status)
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def getParams(self):
        _params = {'data': self.fileToModify.getText(),
                   'replacements': self.replacements.getText(),
                   'dst_file': self.destination.getText(),
                   'columns': self.columns.getText().split('-')}

        return _params

    def execute(self, progress_callback, progress_popup):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("replace_words"):
            if self.can_process:
                params = self.getParams()
                replace_words(**params, progress_callback=progress_callback)
            else:
                progress_popup.emit("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            progress_popup.emit("You are not authorized",
                                "Contact support")


class FindImagesEdit(MainEdit):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.fileToModify.lineEdit.textChanged.connect(self.clearCombos)
        self.button.subscribe(self.start_process)
        self.status.subscribe(self.open_file)

    def setupUi(self):
        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.fileToModify.setBrowseCallback(self.readInputFile)
        self.colCombo1 = ComboInput("Στήλη με το όνομα αναζήτησης:",
                                    size=(150, 150))

        self.destination = FileOutput("Αποθήκευση αρχείου:",
                                      orientation=VERTICAL)

        self.progressBar = ProgressBar()

        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.progressBar)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addWidget(self.colCombo1)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addStretch()
        self.pageLayout.addWidget(self.status)
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def getParams(self):
        _params = {'src': self.fileToModify.getText(),
                   'keyword': self.colCombo1.getCurrentText(),
                   'dst': self.destination.getText()}

        return _params

    def readInputFile(self):
        _file = self.fileToModify.getText()
        if os.path.exists(_file):
            _file_ext = os.path.splitext(_file)[1]
            if _file_ext in ['.xlsx', '.xls']:
                _df = pd.read_excel(_file)
                _cols = _df.columns.tolist()

                self.colCombo1.addItems(_cols)

    def clearCombos(self):
        self.colCombo1.clearItems()

    def execute(self, progress_callback, progress_popup):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("find_images_run"):
            if self.can_process:
                params = self.getParams()
                find_images(**params, progress_callback=progress_callback)
            else:
                progress_popup.emit("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            progress_popup.emit("You are not authorized",
                                "Contact support")


class TitleWordsEdit(MainEdit):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.button.subscribe(self.start_process)
        self.status.subscribe(self.open_file)
        self.can_process = False

    def setupUi(self):
        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.destination = FileOutput("Αποθήκευση επεξεργασμένου αρχείου:",
                                      orientation=VERTICAL)

        self.columns = InputParameter("Στήλες (διαχωρισμένες με παύλα [-])",
                                      orientation=VERTICAL)

        self.progressBar = ProgressBar()

        self.columns.setText("title-meta_title_seo-meta_seo-details")
        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.progressBar)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addWidget(self.columns)
        self.pageLayout.addStretch()
        self.pageLayout.addWidget(self.status)
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def getParams(self):
        _params = {'data': self.fileToModify.getText(),
                   'dst_file': self.destination.getText(),
                   'columns': self.columns.getText().split('-')}

        return _params

    def execute(self, progress_callback, progress_popup):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("title_words"):
            if self.can_process:
                params = self.getParams()
                title_words(**params, progress_callback=progress_callback)
            else:
                progress_popup.emit("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            progress_popup.emit("You are not authorized",
                                "Contact support")


class UpdatePricesEdit(MainEdit):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.fileToModify1.lineEdit.textChanged.connect(self.clearCombos1)
        self.fileToModify2.lineEdit.textChanged.connect(self.clearCombos2)
        self.button.subscribe(self.start_process)
        self.status.subscribe(self.open_file)
        self.can_process = False

    def setupUi(self):
        self.fileToModify1 = FileInput("Αρχείο προς επεξεργασία:",
                                       orientation=VERTICAL)
        self.fileToModify1.setBrowseCallback(self.readInputFile1)
        self.fileToModify2 = FileInput("Αρχείο Γεωργακόπουλου:",
                                       orientation=VERTICAL)
        self.fileToModify2.setBrowseCallback(self.readInputFile2)

        self.colCombo1 = ComboInput("Στήλη με το κωδικό στο αρχείο:",
                                    size=(150, 150))

        self.colCombo2 = ComboInput("Στήλη με το κωδικό στο GBG αρχείο:",
                                    size=(150, 150))

        self.colCombo3 = ComboInput("Στήλη με τη τιμή:",
                                    size=(150, 150))

        self.colCombo4 = ComboInput("Στήλη με τη τιμή στο GBG αρχείο:",
                                    size=(150, 150))

        self.destination = FileOutput("Αποθήκευση επεξεργασμένου αρχείου:",
                                      orientation=VERTICAL)

        self.splitAndPos = InputParameter("Διαχωρισμός και θέση κωδικού:",
                                          orientation=VERTICAL)

        self.splitAndPos.setText("-3")

        self.progressBar = ProgressBar()

        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.progressBar)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify1)
        self.pageLayout.addWidget(self.fileToModify2)
        self.pageLayout.addWidget(self.colCombo1)
        self.pageLayout.addWidget(self.colCombo2)
        self.pageLayout.addWidget(self.colCombo3)
        self.pageLayout.addWidget(self.colCombo4)
        self.pageLayout.addWidget(self.splitAndPos)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addStretch()
        self.pageLayout.addWidget(self.status)
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def getParams(self):
        _params = {'src1': self.fileToModify1.getText(),
                   'src2': self.fileToModify2.getText(),
                   'join_on': self.colCombo2.getCurrentText(),
                   'target_col': self.colCombo3.getCurrentText(),
                   'reference_col': self.colCombo4.getCurrentText(),
                   'pid_col': self.colCombo1.getCurrentText(),
                   'dst_file': self.destination.getText(),
                   'splitter': self.splitAndPos.getText()[0],
                   'index': int(self.splitAndPos.getText()[1]) - 1}

        return _params

    def readInputFile1(self):
        _file = self.fileToModify1.getText()
        if os.path.exists(_file):
            _file_ext = os.path.splitext(_file)[1]
            if _file_ext in ['.xlsx', '.xls']:
                _df = pd.read_excel(_file)
                _cols = _df.columns.tolist()

                self.colCombo1.addItems(_cols)
                self.colCombo3.addItems(_cols)

    def readInputFile2(self):
        _file = self.fileToModify2.getText()
        if os.path.exists(_file):
            _file_ext = os.path.splitext(_file)[1]
            if _file_ext in ['.xlsx', '.xls']:
                _df = pd.read_excel(_file)
                _cols = _df.columns.tolist()

                self.colCombo2.addItems(_cols)
                self.colCombo4.addItems(_cols)

    def clearCombos1(self):
        self.colCombo1.clearItems()
        self.colCombo3.clearItems()

    def clearCombos2(self):
        self.colCombo2.clearItems()
        self.colCombo4.clearItems()

    def execute(self, progress_callback, progress_popup):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("update_prices"):
            if self.can_process:
                params = self.getParams()
                update_from_GBG(**params, progress_callback=progress_callback)
            else:
                progress_popup.emit("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            progress_popup.emit("You are not authorized",
                                "Contact support")


class EditWindow(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWidget")
        self.setStyleSheet(cssGuide)
        self.setWindowTitle("atCrawl Services - Επεξεργασία Αρχείων")
        self.layoutGeneral = QVBoxLayout()
        self.pageCombo = ComboInput('Διαδικασία',
                                    ["Ένωση αρχείων",
                                     "Αλλαγή τιμής σε στήλη",
                                     "Σορτάρισμα αρχείου",
                                     "Κατέβασμα εικόνων",
                                     "Δημιουργία εικόνων (Rellas)",
                                     "Κόψιμο αρχείου",
                                     "Αντικατάσταση λέξεων",
                                     "Αναζήτηση εικόνων (GBG)",
                                     "Αντικατάσταση κεφαλαίων λέξεων",
                                     "Ενημέρωση τιμών GBG"],
                                    size=(100, 200))
        self.pageCombo.subscribe(self.switchPage)
        self.stackedLayout = QStackedLayout()
        self.page1 = MergeEdit()
        self.stackedLayout.addWidget(self.page1)
        self.page2 = FilterEdit()
        self.stackedLayout.addWidget(self.page2)
        self.page3 = SortEdit()
        self.stackedLayout.addWidget(self.page3)
        self.page4 = DownloadImagesEdit()
        self.stackedLayout.addWidget(self.page4)
        self.page5 = CreateImagesEdit()
        self.stackedLayout.addWidget(self.page5)
        self.page6 = SplitFileEdit()
        self.stackedLayout.addWidget(self.page6)
        self.page7 = ReplaceWordsEdit()
        self.stackedLayout.addWidget(self.page7)
        self.page8 = FindImagesEdit()
        self.stackedLayout.addWidget(self.page8)
        self.page9 = TitleWordsEdit()
        self.stackedLayout.addWidget(self.page9)
        self.page10 = UpdatePricesEdit()
        self.stackedLayout.addWidget(self.page10)

        IOWidget.setLastVisit(cwd)

        self.layoutGeneral.addWidget(self.pageCombo)
        self.layoutGeneral.addLayout(self.stackedLayout)
        self.setLayout(self.layoutGeneral)

    def switchPage(self):
        self.stackedLayout.setCurrentIndex(self.pageCombo.getCurrentIndex())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    volume = EditWindow()
    volume.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

from atcrawl.gui.widgets import *
from atcrawl.utilities import *

cwd = paths.get_base_folder()


class SplitFileEdit(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.button.subscribe(self.execute)
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

        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator()
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.status)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addWidget(self.splitRatio)
        self.pageLayout.addStretch()
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def mask_output(self, text=None):
        if text is None:
            self.status.disable()
        else:
            self.status.enable(text)

    def getParams(self):
        _params = {'filepath': self.fileToModify.getText(),
                   'destination': self.destination.getText(),
                   'k': int(self.splitRatio.getText())}

        return _params

    def assert_process_capabilities(self):
        bools = []
        for key, value in self.getParams().items():
            if value:
                bools.append(True)
            else:
                bools.append(False)

        self.can_process = all(bools)

    def execute(self):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed('split_file'):
            if self.can_process:
                params = self.getParams()
                split_file(**params)
                self.mask_output("Ολοκληρώθηκε")
            else:
                show_popup("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            show_popup("You are not authorized",
                       "Contact support")


class DownloadImagesEdit(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.fileToModify.lineEdit.textChanged.connect(self.clearCombos)
        self.button.subscribe(self.execute)
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
                                       orientation=VERTICAL,
                                       )
        self.destination.setText(paths.get_images_export())
        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.status)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addLayout(self.combosLayout)
        self.pageLayout.addWidget(self.prefix)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addStretch()
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def mask_output(self, text=None):
        if text is None:
            self.status.disable()
        else:
            self.status.enable(text)

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

    def assert_process_capabilities(self):
        bools = []
        for key, value in self.getParams().items():
            if value:
                bools.append(True)
            else:
                bools.append(False)

        self.can_process = all(bools)

    def execute(self):
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

                download_images(url_list, dst, name_list)
                df[url_col] = new_names
                df.to_excel(src, index=False)
                self.mask_output("Ολοκληρώθηκε")
            else:
                show_popup("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            show_popup("You are not authorized",
                       "Contact support")


class CreateImagesEdit(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.button.subscribe(self.execute)
        self.can_process = False

    def setupUi(self):
        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.source = FolderInput("Φάκελος πρωτότυπων εικόνων:",
                                  orientation=VERTICAL)
        self.destination = FolderInput("Αποθήκευση αρχέιων στον φάκελο:",
                                       orientation=VERTICAL)
        self.prefix = InputParameter("Link μπροστά από το όνομα της εικόνας:",
                                     orientation=VERTICAL)
        self.source.setText(paths.get_images_import())
        self.destination.setText(paths.get_images_export())
        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.status)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addWidget(self.source)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addWidget(self.prefix)
        self.pageLayout.addStretch()
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def mask_output(self, text=None):
        if text is None:
            self.status.disable()
        else:
            self.status.enable(text)

    def getParams(self):
        _params = {'data': self.fileToModify.getText(),
                   'src_images': self.source.getText(),
                   'dst_images': self.destination.getText(),
                   'prefix_images': self.prefix.getText()}

        return _params

    def assert_process_capabilities(self):
        bools = []
        for key, value in self.getParams().items():
            if key == 'prefix_images':
                continue
            if value:
                bools.append(True)
            else:
                bools.append(False)

        self.can_process = all(bools)

    def execute(self):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("create_images"):
            if self.can_process:
                params = self.getParams()
                create_images(**params)
                self.mask_output("Ολοκληρώθηκε")
            else:
                show_popup("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            show_popup("You are not authorized",
                       "Contact support")


class MergeEdit(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.button.subscribe(self.execute)
        self.can_process = False

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
        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.status)
        self.buttonLayout.addWidget(self.button)
        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.source)
        self.pageLayout.addLayout(self.colsLayout1)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addStretch()
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def mask_output(self, text=None):
        if text is None:
            self.status.disable()
        else:
            self.status.enable(text)

    def getParams(self):
        _params = {'src': self.source.getText(),
                   'col1': self.newColName1.getText(),
                   'val1': self.newColValue1.getText(),
                   'dst': self.destination.getText()}

        return _params

    def assert_process_capabilities(self):
        bools = []
        for key, value in self.getParams().items():
            if key in ['col1', 'val1']:
                continue
            if value:
                bools.append(True)
            else:
                bools.append(False)

        self.can_process = all(bools)

    def execute(self):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("create_images"):
            if self.can_process:
                params = self.getParams()
                merge_file(**params)
                self.mask_output("Ολοκληρώθηκε")
            else:
                show_popup("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            show_popup("You are not authorized",
                       "Contact support")


class FilterEdit(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.fileToModify.lineEdit.textChanged.connect(self.clearCombos)
        self.button.subscribe(self.execute)
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
        self.buttonLayout.addWidget(self.status)
        self.buttonLayout.addWidget(self.button)
        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addLayout(self.horLayout)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addStretch()
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def mask_output(self, text=None):
        if text is None:
            self.status.disable()
        else:
            self.status.enable(text)

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

    def assert_process_capabilities(self):
        bools = []
        for key, value in self.getParams().items():
            if value:
                bools.append(True)
            else:
                bools.append(False)

        self.can_process = all(bools)

    def execute(self):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("filter_run"):
            if self.can_process:
                params = self.getParams()
                filter_file(**params)
                self.mask_output("Ολοκληρώθηκε")
            else:
                show_popup("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            show_popup("You are not authorized",
                       "Contact support")


class SortEdit(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.fileToModify.lineEdit.textChanged.connect(self.clearCombos)
        self.button.subscribe(self.execute)
        self.can_process = False

    def setupUi(self):
        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.fileToModify.setBrowseCallback(self.readInputFile)
        self.colCombo1 = ComboInput("Στήλη εφαρμογής", size=(150, 150))

        self.destination = FileOutput("Αποθήκευση αρχείου:",
                                      orientation=VERTICAL)

        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.status)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addWidget(self.colCombo1)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addStretch()
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def mask_output(self, text=None):
        if text is None:
            self.status.disable()
        else:
            self.status.enable(text)

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

    def assert_process_capabilities(self):
        bools = []
        for key, value in self.getParams().items():
            if value:
                bools.append(True)
            else:
                bools.append(False)

        self.can_process = all(bools)

    def execute(self):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("sort_run"):
            if self.can_process:
                params = self.getParams()
                sort_file(**params)
                self.mask_output("Ολοκληρώθηκε")
            else:
                show_popup("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            show_popup("You are not authorized",
                       "Contact support")


class ReplaceWordsEdit(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.button.subscribe(self.execute)
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

        self.replacements.setText(paths.get_replacements())
        self.columns.setText("title-meta_title_seo-meta_seo-details")
        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.status)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addWidget(self.replacements)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addWidget(self.columns)
        self.pageLayout.addStretch()
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def mask_output(self, text=None):
        if text is None:
            self.status.disable()
        else:
            self.status.enable(text)

    def getParams(self):
        _params = {'data': self.fileToModify.getText(),
                   'replacements': self.replacements.getText(),
                   'dst_file': self.destination.getText(),
                   'columns': self.columns.getText().split('-')}

        return _params

    def assert_process_capabilities(self):
        bools = []
        for key, value in self.getParams().items():
            if value:
                bools.append(True)
            else:
                bools.append(False)

        self.can_process = all(bools)

    def execute(self):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("replace_words"):
            if self.can_process:
                params = self.getParams()
                replace_words(**params)
                self.mask_output("Ολοκληρώθηκε")
            else:
                show_popup("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            show_popup("You are not authorized",
                       "Contact support")


class FindImagesEdit(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.fileToModify.lineEdit.textChanged.connect(self.clearCombos)
        self.button.subscribe(self.execute)
        self.can_process = False

    def setupUi(self):
        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.fileToModify.setBrowseCallback(self.readInputFile)
        self.colCombo1 = ComboInput("Στήλη με το όνομα αναζήτησης:",
                                    size=(150, 150))

        self.destination = FileOutput("Αποθήκευση αρχείου:",
                                      orientation=VERTICAL)

        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='')
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.status)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addWidget(self.colCombo1)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addStretch()
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def mask_output(self, text=None):
        if text is None:
            self.status.disable()
        else:
            self.status.enable(text)

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

    def assert_process_capabilities(self):
        bools = []
        for key, value in self.getParams().items():
            if value:
                bools.append(True)
            else:
                bools.append(False)

        self.can_process = all(bools)

    def execute(self):
        self.assert_process_capabilities()
        if authorizer.user_is_licensed("find_images_run"):
            if self.can_process:
                params = self.getParams()
                find_images(**params)
                self.mask_output("Ολοκληρώθηκε")
            else:
                show_popup("Συμπλήρωσε τα απαραίτητα πεδία")
        else:
            show_popup("You are not authorized",
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
                                     "Αναζήτηση εικόνων (GBG)"],
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

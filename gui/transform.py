# -*- coding: utf-8 -*-

from atcrawl.core.sql import AtcrawlSQL
from atcrawl.crawlers import *
from atcrawl.core.engine import *
from atcrawl.utilities.auth import *
from atcrawl.utilities.paths import *
from atcrawl.gui.welcome_design import *
from atcrawl.gui.widgets import *
from subprocess import Popen

db_browser = "C:/Program Files/DB Browser for SQLite/DB Browser for SQLite.exe"


class TransformUI(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(TransformUI, self).__init__(parent=parent, *args, **kwargs)
        self.sql = AtcrawlSQL(str(paths.get_db()))
        self.all_jobs = [''] + list(map(str, self.sql.get_all_jobid()))

        self.setupUi()

        self.auth = None

        self.file_name = None
        self.folder_name = None
        self.output = None
        self.site = None
        self.data = None
        self.job_id = None
        self.site = None
        self.date = None
        self.items = None
        self.params = None
        self.meta_mapping = {'meta0': self.inputMeta0,
                             'meta1': self.inputMeta1,
                             'meta2': self.inputMeta2,
                             'meta3': self.inputMeta3,
                             'meta4': self.inputMeta4,
                             'meta5': self.inputMeta5,
                             'meta6': self.inputMeta6,
                             'meta7': self.inputMeta7,
                             'meta_check': self.checkMeta}

        self.statusGeneral.subscribe(self.open_file)
        self.buttonDb.subscribe(self.open_db)
        self.comboJob.subscribe(self.load)
        self.buttonTransform.subscribe(self.transform)

        self.outputFolder.setText(paths.get_default_export())

    def setupUi(self):
        self.setObjectName("MainWidget")
        self.setStyleSheet(cssGuide)
        self.setWindowTitle("atCrawl Services")
        self.resize(500, 350)

        # self.comboJob = ComboInput('Job ID',items=all_jobs, size=(70, 100))
        self.comboJob = ComboInput('Job ID', items=self.all_jobs, size=(70, 50))
        self.statusSite = InputParameter('Site', size=(50, 100))
        self.statusDate = InputParameter('Date', size=(50, 100))
        self.statusItems = InputParameter('Items', size=(50, 100))
        self.statusGeneral = StatusIndicator()

        self.buttonDb = Button('open DB')
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

        self.layoutGui = QHBoxLayout()
        self.layoutLeft = QVBoxLayout()
        self.layoutTop = QHBoxLayout()
        self.layoutParams = QHBoxLayout()
        self.layoutSmall = QVBoxLayout()
        self.layoutBig = QVBoxLayout()
        self.layoutBottom = QVBoxLayout()
        self.layoutButtons = QVBoxLayout()
        self.layoutStatus = QHBoxLayout()
        self.layoutTop.addWidget(self.comboJob)
        self.layoutTop.addWidget(self.statusSite, 1)
        self.layoutTop.addWidget(self.statusDate, 1)
        self.layoutTop.addWidget(self.statusItems)

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

        self.layoutButtons.addWidget(self.buttonDb)
        self.layoutButtons.addWidget(self.buttonTransform)

        self.layoutStatus.addWidget(self.statusGeneral)

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
        try:
            self.job_id = int(self.comboJob.getCurrentText())
            jobid_params = self.sql.get_params_from_jobid(self.job_id)

            self.site = jobid_params[0]
            self.date = jobid_params[1]
            self.items = str(jobid_params[2])
            self.params = eval(jobid_params[3])

            self.statusSite.setText(self.site)
            self.statusDate.setText(self.date)
            self.statusItems.setText(self.items)

            self.show_all_widgets()

            for key, value in self.params.items():
                if key == 'meta_check':
                    self.checkMeta.setChecked(value)
                else:
                    self.meta_mapping[key].setText(value)

            self.apply_masks()
        except ValueError:
            pass

    def transform(self):
        if authorizer.user_is_licensed('transform'):
            _name = self.get_filename()
            _folder = self.get_folder()
            _type = 'xlsx'
            _output = _folder + f'/{_name}.{_type}'

            table = self.site.split('.')[0]
            query_result = self.sql.get_records_from_jobid(table, self.job_id)
            self.transformer = transform_map[self.site].from_db(query_result)
            self.data = self.transformer.transform(**self.get_params())

            self.export(name=_name,
                        folder=_folder,
                        export_type=_type)

            self.output = _output

            self.mask_output(f"{_output}")
        else:
            show_popup.emit("You are not authorized",
                            "Contact support")

    def export(self, name, folder, export_type):
        if self.data is not None:
            if export_type == 'csv':
                dst = Path(folder).joinpath(f'{name}.csv')
                self.data.to_csv(dst, index=False, sep=';')
                print(f"\nExported csv file at:\n -> {dst}\n")
            else:
                dst = Path(folder).joinpath(f'{name}.xlsx')
                self.data.to_excel(dst, index=False)
                print(f"\nExported excel file at:\n -> {dst}\n")

    def open_file(self):
        if self.output is not None:
            os.startfile(self.output)

    def open_db(self):
        Popen([db_browser, str(paths.get_db())])

    def set_auth(self, authorizer):
        self.auth = authorizer

    def show_all_widgets(self):
        for wi in self.meta_mapping:
            self.meta_mapping[wi].show()

    def apply_masks(self):
        if self.site == 'antallaktikaonline.gr':
            self.inputMeta0.setLabel("Brand")
            self.inputMeta1.setLabel("Car")
            self.inputMeta2.hide()
            self.inputMeta3.setLabel("Price (%)")
            self.inputMeta4.hide()
            self.inputMeta5.hide()
            self.inputMeta6.hide()
            self.inputMeta7.hide()
            self.checkMeta.hide()
            self.inputMeta0.setCompleter(MANUFACTURES_BRANDS)

        if self.site == 'skroutz.gr':
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
            self.inputMeta0.setCompleter(MANUFACTURES_BRANDS)

        if self.site == 'rellasamortiser.gr':
            self.inputMeta0.setLabel("Brand")
            self.inputMeta1.setLabel("Model")
            self.inputMeta2.setLabel("ID Cat.")
            self.inputMeta3.setLabel("Price (%)")
            self.inputMeta4.setLabel("Skroutz")
            self.inputMeta5.setLabel("Meta Title SEO")
            self.inputMeta6.setLabel("Meta SEO")
            self.inputMeta7.setLabel("Extra Details")
            self.checkMeta.hide()
            self.inputMeta0.setCompleter(CAR_BRANDS)

        if self.site == 'gbg-eshop.gr':
            self.inputMeta0.setLabel("Brand")
            self.inputMeta1.setLabel("Model")
            self.inputMeta2.setLabel("ID Cat.")
            self.inputMeta3.setLabel("Price (%)")
            self.inputMeta4.setLabel("Πρόθεμα")
            self.inputMeta5.setLabel("Χρονολογία")
            self.inputMeta6.setLabel("Meta Title SEO")
            self.inputMeta7.setLabel("Meta SEO")

            self.checkMeta.hide()
            self.inputMeta0.setCompleter(CAR_BRANDS)

    def mask_output(self, text=None):
        if text is None:
            self.statusGeneral.disable()
        else:
            self.statusGeneral.enable(text)

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


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    volume = TransformUI()
    volume.show()
    sys.exit(app.exec_())

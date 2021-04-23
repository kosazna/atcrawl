from PyQt5 import QtCore, QtGui, QtWidgets
from atcrawl.gui.colors import *

HEIGHT = 25
HOFFSET = 55
BTWIDTH = 100
FONTSIZE = 10
FONT = "Segoe UI"
HORIZONTAL = 'H'
VERTICAL = 'V'
PATH_PLACEHOLDER = "Paste path here or browse..."


class FileNameInput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 placeholder='',
                 *args,
                 **kwargs):
        super(FileNameInput, self).__init__(*args, **kwargs)
        self.setupUi(label, placeholder)

    def setupUi(self, label, placeholder):
        font = QtGui.QFont()
        font.setFamily(FONT)
        font.setPointSize(FONTSIZE)

        regexp = QtCore.QRegExp('[^\.\<\>:\"/\\\|\?\*]*')
        validator = QtGui.QRegExpValidator(regexp)

        self.label = QtWidgets.QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(font)
        self.label.setMinimumWidth(HOFFSET)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setFont(font)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet())
        self.lineEdit.setValidator(validator)
        self.setPlaceholder(placeholder)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

    def getText(self):
        return self.lineEdit.text()

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)

    def setMaximumWidth(self, maxw):
        self.lineEdit.setMaximumWidth(maxw)

    def setMinimumWidth(self, minw):
        self.lineEdit.setMinimumWidth(minw)


class FolderInput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 placeholder=PATH_PLACEHOLDER,
                 *args,
                 **kwargs):
        super(FolderInput, self).__init__(*args, **kwargs)
        self.setupUi(label, placeholder)
        self.lastVisit = ''
        self.button.clicked.connect(self.browse)

    def setupUi(self, label, placeholder):
        labelFont = QtGui.QFont()
        labelFont.setFamily(FONT)
        labelFont.setPointSize(FONTSIZE)
        btFont = QtGui.QFont()
        btFont.setFamily(FONT)
        btFont.setPointSize(FONTSIZE)
        btFont.setBold(True)
        self.label = QtWidgets.QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(labelFont)
        self.label.setMinimumWidth(HOFFSET)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet())
        self.setPlaceholder(placeholder)
        self.button = QtWidgets.QToolButton()
        self.button.setFont(btFont)
        self.button.setFixedHeight(HEIGHT)
        self.button.setFixedWidth(HEIGHT)
        self.button.setText("...")
        self.button.setStyleSheet(make_stylesheet())
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def browse(self):
        file_path = QtWidgets.QFileDialog.getExistingDirectory(
            directory=self.lastVisit)
        if file_path:
            self.lineEdit.setText(file_path)
            self.lastVisit = file_path

    def getText(self):
        return self.lineEdit.text()

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)


class FileInput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 placeholder=PATH_PLACEHOLDER,
                 *args,
                 **kwargs):
        super(FileInput, self).__init__(*args, **kwargs)
        self.setupUi(label, placeholder)
        self.lastVisit = ''
        self.button.clicked.connect(self.browse)

    def setupUi(self, label, placeholder):
        labelFont = QtGui.QFont()
        labelFont.setFamily(FONT)
        labelFont.setPointSize(FONTSIZE)
        btFont = QtGui.QFont()
        btFont.setFamily(FONT)
        btFont.setPointSize(FONTSIZE)
        btFont.setBold(True)
        self.label = QtWidgets.QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(labelFont)
        self.label.setMinimumWidth(HOFFSET)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet())
        self.setPlaceholder(placeholder)
        self.button = QtWidgets.QToolButton()
        self.button.setFont(btFont)
        self.button.setFixedHeight(HEIGHT)
        self.button.setFixedWidth(HEIGHT)
        self.button.setText("...")
        self.button.setStyleSheet(make_stylesheet())
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def browse(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            directory=self.lastVisit)
        file_path = filename[0]
        if file_path:
            self.lineEdit.setText(file_path)
            self.lastVisit = file_path

    def getText(self):
        return self.lineEdit.text()

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)


class FileOutput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 placeholder=PATH_PLACEHOLDER,
                 *args,
                 **kwargs):
        super(FileOutput, self).__init__(*args, **kwargs)
        self.setupUi(label, placeholder)
        self.lastVisit = ''
        self.button.clicked.connect(self.browse)

    def setupUi(self, label, placeholder):
        font = QtGui.QFont()
        font.setFamily(FONT)
        font.setPointSize(FONTSIZE)
        self.label = QtWidgets.QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(font)
        self.label.setMinimumWidth(HOFFSET)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setFont(font)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet())
        self.setPlaceholder(placeholder)
        font.setBold(True)
        self.button = QtWidgets.QToolButton()
        self.button.setFont(font)
        self.button.setFixedHeight(HEIGHT)
        self.button.setFixedWidth(HEIGHT)
        self.button.setText("...")
        self.button.setStyleSheet(make_stylesheet())
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit, 2)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def browse(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(
            directory=self.lastVisit)
        file_path = filename[0]
        if file_path:
            self.lineEdit.setText(file_path)
            self.lastVisit = file_path

    def getText(self):
        return self.lineEdit.text()

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)


class InputParameter(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 orientation=HORIZONTAL,
                 *args,
                 **kwargs):
        super(InputParameter, self).__init__(*args, **kwargs)
        self.setupUi(label, orientation)

    def setupUi(self, label, orientation):
        font = QtGui.QFont()
        font.setFamily(FONT)
        font.setPointSize(FONTSIZE)
        self.label = QtWidgets.QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(font)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setFont(font)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet())
        if orientation == VERTICAL:
            layout = QtWidgets.QVBoxLayout()
        else:
            layout = QtWidgets.QHBoxLayout()
            self.label.setMinimumWidth(HOFFSET)
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

    def disable(self):
        self.lineEdit.setEnabled(False)
        self.lineEdit.setStyleSheet(make_stylesheet(dark))

    def enable(self):
        self.lineEdit.setEnabled(True)
        self.lineEdit.setStyleSheet(make_stylesheet(white))

    def setText(self, text):
        self.lineEdit.setText(text)

    def setLabel(self, text):
        self.label.setText(text)

    def getText(self):
        return self.lineEdit.text()

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setMaximumWidth(self, maxw):
        self.lineEdit.setMaximumWidth(maxw)

    def setMinimumWidth(self, minw):
        self.lineEdit.setMinimumWidth(minw)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)


class IntInputParameter(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 orientation=HORIZONTAL,
                 value_range=None,
                 *args,
                 **kwargs):
        super(IntInputParameter, self).__init__(*args, **kwargs)
        self.setupUi(label, orientation, value_range)

    def setupUi(self, label, orientation, value_range):
        font = QtGui.QFont()
        font.setFamily(FONT)
        font.setPointSize(FONTSIZE)
        self.label = QtWidgets.QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(font)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.validator = QtGui.QIntValidator()
        if value_range is not None:
            self.validator.setRange(*value_range)
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setFont(font)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet())
        self.lineEdit.setValidator(self.validator)
        if orientation == VERTICAL:
            layout = QtWidgets.QVBoxLayout()
        else:
            layout = QtWidgets.QHBoxLayout()
            self.label.setMinimumWidth(HOFFSET)
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

    def disable(self):
        self.lineEdit.setEnabled(False)
        self.lineEdit.setStyleSheet(make_stylesheet(dark))

    def enable(self):
        self.lineEdit.setEnabled(True)
        self.lineEdit.setStyleSheet(make_stylesheet(white))

    def setText(self, text):
        self.lineEdit.setText(text)

    def setLabel(self, text):
        self.label.setText(text)

    def getText(self):
        return self.lineEdit.text()

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setMaximumWidth(self, maxw):
        self.lineEdit.setMaximumWidth(maxw)

    def setMinimumWidth(self, minw):
        self.lineEdit.setMinimumWidth(minw)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)


class ComboInput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 items=None,
                 *args,
                 **kwargs):
        super(ComboInput, self).__init__(*args, **kwargs)
        self.setupUi(label, items)

    def setupUi(self, label, items):
        font = QtGui.QFont()
        font.setFamily(FONT)
        font.setPointSize(FONTSIZE)
        self.label = QtWidgets.QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(font)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.label.setMinimumWidth(HOFFSET)
        self.comboEdit = QtWidgets.QComboBox()
        self.comboEdit.setFont(font)
        self.comboEdit.setFixedHeight(HEIGHT)
        self.comboEdit.setStyleSheet(make_stylesheet())
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.comboEdit, 1)
        self.setLayout(layout)
        if items is not None:
            for item in items:
                self.comboEdit.addItem(item)

    def getCurrentText(self):
        return self.comboEdit.currentText()

    def subscribe(self, func):
        self.comboEdit.currentIndexChanged.connect(func)


class CheckInput(QtWidgets.QCheckBox):
    def __init__(self, label='', checked=True, *args, **kwargs):
        super(CheckInput, self).__init__(*args, **kwargs)
        self.setupUi(label, checked)

    def setupUi(self, label, checked):
        font = QtGui.QFont()
        font.setFamily(FONT)
        font.setPointSize(FONTSIZE)
        self.setText(label)
        self.setFixedHeight(HEIGHT)
        self.setFont(font)
        self.setChecked(checked)
        self.setStyleSheet(make_stylesheet(white, alpha=0))

    def enable(self, text=''):
        self.setEnabled(True)
        self.setText(text)

    def disable(self):
        self.setEnabled(False)
        self.setText('')

    def subscribe(self, func):
        self.stateChanged.connect(func)


class Button(QtWidgets.QToolButton):
    def __init__(self, label='', *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.setupUi(label)

    def setupUi(self, label):
        font = QtGui.QFont()
        font.setFamily(FONT)
        font.setPointSize(FONTSIZE)
        font.setBold(True)
        self.setText(label)
        self.setFixedHeight(HEIGHT)
        self.setFont(font)
        self.setStyleSheet(make_stylesheet(blue, radius=5))
        self.setMinimumWidth(BTWIDTH)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def disable(self):
        self.setEnabled(False)
        self.setStyleSheet(make_stylesheet(grey))
        self.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

    def enable(self, color):
        self.setEnabled(True)
        self.setStyleSheet(make_stylesheet(color))
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def subscribe(self, func):
        self.clicked.connect(func)

    def setStyle(self, style):
        self.setStyleSheet(style)


class StatusIndicator(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 status='',
                 size=BTWIDTH,
                 *args,
                 **kwargs):
        super(StatusIndicator, self).__init__(*args, **kwargs)
        self.setupUi(label, status, size)

    def setupUi(self, label, status, size):
        layout = QtWidgets.QHBoxLayout()
        labelFont = QtGui.QFont()
        labelFont.setFamily(FONT)
        labelFont.setPointSize(FONTSIZE)
        btFont = QtGui.QFont()
        btFont.setFamily(FONT)
        btFont.setPointSize(FONTSIZE)
        btFont.setBold(True)
        if label:
            self.label = QtWidgets.QLabel()
            self.label.setFont(labelFont)
            self.label.setText(label)
            self.label.setStyleSheet(make_stylesheet(alpha=0))
            self.label.setFixedHeight(HEIGHT)
            self.label.setFixedWidth(HOFFSET)
            layout.addWidget(self.label)
        self.button = QtWidgets.QToolButton()
        self.button.setFont(btFont)
        self.button.setText(status)
        self.button.setFixedHeight(HEIGHT)
        self.button.setMinimumWidth(size)
        self.button.setEnabled(False)
        self.button.setStyleSheet(make_stylesheet(grey, radius=5))
        layout.addWidget(self.button)
        self.setLayout(layout)

    def disable(self):
        self.button.setEnabled(False)
        self.button.setText('')
        self.button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

    def enable(self, text=''):
        self.button.setEnabled(True)
        self.button.setText(text)
        self.button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def setText(self, text):
        self.button.setText(text)

    def setStyle(self, style):
        self.button.setStyleSheet(style)

    def subscribe(self, func):
        self.button.clicked.connect(func)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)


class CrawlerUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(CrawlerUI, self).__init__(*args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.setStyleSheet(make_color(light_grey))
        self.setWindowTitle("atCrawl Services")
        self.resize(550, 450)
        self.buttonLaunch = Button('launch')
        self.buttonCollect = Button('collect')
        self.buttonStop = Button('stop')
        self.buttonReset = Button('reset')
        self.buttonTerminate = Button('terminate')
        self.checkMeta = CheckInput('MetaCheck')
        self.inputUrl = InputParameter('URL')
        self.inputMeta0 = InputParameter('Meta0')
        self.inputMeta0.setMinimumWidth(200)
        self.inputMeta1 = InputParameter('Meta1')
        self.inputMeta1.setMinimumWidth(200)
        self.inputMeta2 = InputParameter('Meta2')
        self.inputMeta2.setMinimumWidth(200)
        self.inputMeta3 = IntInputParameter('Meta3', value_range=(-99, 99))
        self.inputMeta3.setMinimumWidth(200)
        self.inputMeta4 = InputParameter('Meta4')
        self.inputMeta4.setOffset(100)
        self.inputMeta5 = InputParameter('Meta5')
        self.inputMeta5.setOffset(100)
        self.inputMeta6 = InputParameter('Meta6')
        self.inputMeta6.setOffset(100)
        self.inputMeta7 = InputParameter('Meta7')
        self.inputMeta7.setOffset(100)
        self.inputFilename = FileNameInput('Filename')
        self.inputFilename.setMinimumWidth(200)
        self.outputFolder = FolderInput('Folder')
        self.outputFolder.setOffset(100)
        self.statusBrowser = StatusIndicator('Browser', 'offline')
        self.statusCrawler = StatusIndicator('Crawler', 'offline')
        self.statusGeneral = StatusIndicator(status='', size=self.width())
        self.layoutGui = QtWidgets.QHBoxLayout()
        self.layoutLeft = QtWidgets.QVBoxLayout()
        self.layoutTop = QtWidgets.QHBoxLayout()
        self.layoutParams = QtWidgets.QHBoxLayout()
        self.layoutSmall = QtWidgets.QVBoxLayout()
        self.layoutBig = QtWidgets.QVBoxLayout()
        self.layoutBottom = QtWidgets.QVBoxLayout()
        self.layoutButtons = QtWidgets.QVBoxLayout()
        self.layoutStatus = QtWidgets.QHBoxLayout()
        self.layoutTop.addWidget(self.inputUrl)
        self.layoutSmall.addWidget(self.inputMeta0, 0, QtCore.Qt.AlignLeft)
        self.layoutSmall.addWidget(self.inputMeta1, 0, QtCore.Qt.AlignLeft)
        self.layoutSmall.addWidget(self.inputMeta2, 0, QtCore.Qt.AlignLeft)
        self.layoutSmall.addWidget(self.inputMeta3, 0, QtCore.Qt.AlignLeft)
        self.layoutSmall.addWidget(self.inputFilename, 0, QtCore.Qt.AlignLeft)
        self.layoutBig.addWidget(self.inputMeta4)
        self.layoutBig.addWidget(self.inputMeta5)
        self.layoutBig.addWidget(self.inputMeta6)
        self.layoutBig.addWidget(self.inputMeta7)
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


app = QtWidgets.QApplication([])
volume = CrawlerUI()
volume.show()
app.exec_()

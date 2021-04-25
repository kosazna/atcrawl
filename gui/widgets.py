# -*- coding: utf-8 -*-


import os

import pandas as pd
from atcrawl.gui.colors import *
from atcrawl.utilities import *
from atcrawl.gui.qutils import show_popup
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QCursor, QFont, QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                             QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QSizePolicy, QStackedLayout, QToolButton,
                             QVBoxLayout, QWidget)

HEIGHT = 25
HOFFSET = 55
BTWIDTH = 80
FONTSIZE = 10
FONT = "Segoe UI"
HORIZONTAL = 'H'
VERTICAL = 'V'
PATH_PLACEHOLDER = "Paste path here or browse..."

labelFont = QFont()
labelFont.setFamily(FONT)
labelFont.setPointSize(FONTSIZE)
btFont = QFont()
btFont.setFamily(FONT)
btFont.setPointSize(FONTSIZE)
btFont.setBold(True)

cwd = str(paths.get_cwd())


class FileNameInput(QWidget):
    def __init__(self,
                 label='',
                 placeholder='',
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder)

    def setupUi(self, label, placeholder):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(labelFont)
        self.label.setMinimumWidth(HOFFSET)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.lineEdit = QLineEdit()
        self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet(border=grey))
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        regexp = QRegExp('[^\.\<\>:\"/\\\|\?\*]*')
        validator = QRegExpValidator(regexp, self.lineEdit)
        self.lineEdit.setValidator(validator)
        self.setPlaceholder(placeholder)
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

    def getText(self, suffix=None):
        if suffix is not None:
            _stem = self.lineEdit.text()
            _suffix = suffix if suffix.startswith('.') else f".{suffix}"
            _filename = f"{_stem}{_suffix}"
            return _filename
        return self.lineEdit.text()

    def setText(self, text):
        self.lineEdit.setText(text)

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)

    def setMaximumWidth(self, maxw):
        self.lineEdit.setMaximumWidth(maxw)

    def setMinimumWidth(self, minw):
        self.lineEdit.setMinimumWidth(minw)


class FolderInput(QWidget):
    def __init__(self,
                 label='',
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 orientation=HORIZONTAL,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, orientation)
        self.lastVisit = cwd
        self.button.clicked.connect(self.browse)
        self.lineEdit.textChanged.connect(lambda x: self.pathExists(x))

    def setupUi(self, label, placeholder, orientation):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(labelFont)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.lineEdit = QLineEdit()
        self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet(border=grey))
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setPlaceholder(placeholder)
        self.button = QToolButton()
        self.button.setFont(btFont)
        self.button.setFixedHeight(HEIGHT)
        self.button.setFixedWidth(HEIGHT)
        self.button.setText("...")
        self.button.setStyleSheet(make_stylesheet(border=grey))
        if orientation == HORIZONTAL:
            self.label.setMinimumWidth(HOFFSET)
            layout = QHBoxLayout()
            layout.addWidget(self.label)
            layout.addWidget(self.lineEdit)
            layout.addWidget(self.button)
        else:
            layout = QVBoxLayout()
            inner = QHBoxLayout()
            layout.addWidget(self.label)
            inner.addWidget(self.lineEdit)
            inner.addWidget(self.button)
            layout.addLayout(inner)
        self.setLayout(layout)

    def browse(self):
        file_path = QFileDialog.getExistingDirectory(directory=self.lastVisit)
        if file_path:
            self.lineEdit.setText(file_path)
            self.lastVisit = file_path

    def getText(self):
        return self.lineEdit.text()

    def setText(self, text):
        self.lineEdit.setText(text)
        self.lastVisit = text

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)

    def pathExists(self, path):
        if path:
            if os.path.exists(path):
                if os.path.isdir(path):
                    self.lineEdit.setStyleSheet(make_stylesheet(border=green))
                else:
                    self.lineEdit.setStyleSheet(make_stylesheet(border=yellow))
            else:
                self.lineEdit.setStyleSheet(make_stylesheet(border=red))
        else:
            self.lineEdit.setStyleSheet(make_stylesheet(border=grey))


class FileInput(QWidget):
    def __init__(self,
                 label='',
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 orientation=HORIZONTAL,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, orientation)
        self.lastVisit = cwd
        self.button.clicked.connect(self.browse)
        self.lineEdit.textChanged.connect(lambda x: self.pathExists(x))
        self.browseCallback = None

    def setupUi(self, label, placeholder, orientation):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(labelFont)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.lineEdit = QLineEdit()
        self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet(border=grey))
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setPlaceholder(placeholder)
        self.button = QToolButton()
        self.button.setFont(btFont)
        self.button.setFixedHeight(HEIGHT)
        self.button.setFixedWidth(HEIGHT)
        self.button.setText("...")
        self.button.setStyleSheet(make_stylesheet(border=grey))
        if orientation == HORIZONTAL:
            self.label.setMinimumWidth(HOFFSET)
            layout = QHBoxLayout()
            layout.addWidget(self.label)
            layout.addWidget(self.lineEdit)
            layout.addWidget(self.button)
        else:
            layout = QVBoxLayout()
            inner = QHBoxLayout()
            layout.addWidget(self.label)
            inner.addWidget(self.lineEdit)
            inner.addWidget(self.button)
            layout.addLayout(inner)
        self.setLayout(layout)
        self.setLayout(layout)

    def browse(self):
        filename = QFileDialog.getOpenFileName(directory=self.lastVisit)
        file_path = filename[0]
        if file_path:
            self.lineEdit.setText(file_path)
            self.lastVisit = file_path

            if self.browseCallback is not None:
                self.browseCallback()

    def setBrowseCallback(self, func):
        self.browseCallback = func

    def getText(self):
        return self.lineEdit.text()

    def setText(self, text):
        self.lineEdit.setText(text)
        self.lastVisit = text

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)

    def pathExists(self, path):
        if path:
            if os.path.exists(path):
                if os.path.isfile(path):
                    self.lineEdit.setStyleSheet(make_stylesheet(border=green))
                else:
                    self.lineEdit.setStyleSheet(make_stylesheet(border=yellow))
            else:
                self.lineEdit.setStyleSheet(make_stylesheet(border=red))
        else:
            self.lineEdit.setStyleSheet(make_stylesheet(border=grey))


class FileOutput(QWidget):
    def __init__(self,
                 label='',
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 orientation=HORIZONTAL,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, orientation)
        self.lastVisit = cwd
        self.button.clicked.connect(self.browse)

    def setupUi(self, label, placeholder, orientation):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(labelFont)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.lineEdit = QLineEdit()
        self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet(border=grey))
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setPlaceholder(placeholder)
        self.button = QToolButton()
        self.button.setFont(btFont)
        self.button.setFixedHeight(HEIGHT)
        self.button.setFixedWidth(HEIGHT)
        self.button.setText("...")
        self.button.setStyleSheet(make_stylesheet(border=grey))
        if orientation == HORIZONTAL:
            self.label.setMinimumWidth(HOFFSET)
            layout = QHBoxLayout()
            layout.addWidget(self.label)
            layout.addWidget(self.lineEdit)
            layout.addWidget(self.button)
        else:
            layout = QVBoxLayout()
            inner = QHBoxLayout()
            layout.addWidget(self.label)
            inner.addWidget(self.lineEdit)
            inner.addWidget(self.button)
            layout.addLayout(inner)
        self.setLayout(layout)

    def browse(self):
        filename = QFileDialog.getSaveFileName(directory=self.lastVisit)
        file_path = filename[0]
        if file_path:
            self.lineEdit.setText(file_path)
            self.lastVisit = file_path

    def getText(self):
        return self.lineEdit.text()

    def setText(self, text):
        self.lineEdit.setText(text)
        self.lastVisit = text

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)


class InputParameter(QWidget):
    def __init__(self,
                 label='',
                 orientation=HORIZONTAL,
                 parent=None,
                 completer=None,
                 hidden=False,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, orientation, hidden)
        self.setCompleter(completer)

    def setupUi(self, label, orientation, hidden):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(labelFont)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.lineEdit = QLineEdit()
        self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet(border=grey))
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        if hidden:
            self.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        if orientation == VERTICAL:
            layout = QVBoxLayout()
        else:
            layout = QHBoxLayout()
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

    def setCompleter(self, items):
        if items is not None:
            _completer = QCompleter(items)
            _completer.setCompletionMode(QCompleter.PopupCompletion)
            _completer.setCaseSensitivity(Qt.CaseInsensitive)
            _completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
            _completer.setFilterMode(Qt.MatchContains)
            _completer.popup().setStyleSheet(make_stylesheet(border=grey))
            self.lineEdit.setCompleter(_completer)


class IntInputParameter(QWidget):
    def __init__(self,
                 label='',
                 orientation=HORIZONTAL,
                 value_range=None,
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, orientation, value_range)

    def setupUi(self, label, orientation, value_range):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(labelFont)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.validator = QIntValidator()
        if value_range is not None:
            self.validator.setRange(*value_range)
        self.lineEdit = QLineEdit()
        self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet(border=grey))
        self.lineEdit.setValidator(self.validator)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        if orientation == VERTICAL:
            layout = QVBoxLayout()
        else:
            layout = QHBoxLayout()
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


class ComboInput(QWidget):
    def __init__(self,
                 label='',
                 items=None,
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, items)

    def setupUi(self, label, items):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(labelFont)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.label.setMinimumWidth(HOFFSET)
        self.comboEdit = QComboBox()
        self.comboEdit.setFont(labelFont)
        self.comboEdit.setFixedHeight(HEIGHT)
        self.comboEdit.setStyleSheet(make_stylesheet(border=grey))
        self.comboEdit.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents)
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.comboEdit, 1)
        self.setLayout(layout)
        if items is not None:
            self.comboEdit.addItems(items)

    def getCurrentText(self):
        return self.comboEdit.currentText()

    def getCurrentIndex(self):
        return self.comboEdit.currentIndex()

    def addItems(self, items):
        self.comboEdit.addItems(items)

    def clearItems(self):
        self.comboEdit.clear()

    def setOffset(self, offset):
        self.label.setMinimumWidth(offset)

    def subscribe(self, func):
        self.comboEdit.currentIndexChanged.connect(func)


class CheckInput(QCheckBox):
    def __init__(self, label='', checked=True, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, checked)

    def setupUi(self, label, checked):
        self.setText(label)
        self.setFixedHeight(HEIGHT)
        self.setFont(labelFont)
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


class Button(QToolButton):
    def __init__(self, label='', parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label)

    def setupUi(self, label):
        self.setText(label)
        self.setFixedHeight(HEIGHT)
        self.setFont(btFont)
        self.setStyleSheet(make_stylesheet(blue, radius=5))
        self.setMinimumWidth(BTWIDTH)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        # self.setCheckable(True)

    def disable(self):
        self.setEnabled(False)
        self.setStyleSheet(make_stylesheet(grey))
        self.setCursor(QCursor(Qt.ForbiddenCursor))

    def enable(self, color):
        self.setEnabled(True)
        self.setStyleSheet(make_stylesheet(color))
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def subscribe(self, func):
        self.clicked.connect(func)

    def setStyle(self, style):
        self.setStyleSheet(style)


class StatusIndicator(QWidget):
    def __init__(self,
                 label='',
                 status='',
                 size=BTWIDTH,
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, status, size)

    def setupUi(self, label, status, size):
        layout = QHBoxLayout()
        if label:
            self.label = QLabel()
            self.label.setFont(labelFont)
            self.label.setText(label)
            self.label.setStyleSheet(make_stylesheet(alpha=0))
            self.label.setFixedHeight(HEIGHT)
            self.label.setFixedWidth(HOFFSET)
            layout.addWidget(self.label)
        self.button = QToolButton()
        self.button.setFont(btFont)
        self.button.setText(status)
        self.button.setFixedHeight(HEIGHT)
        self.button.setMinimumWidth(size)
        self.button.setEnabled(False)
        self.button.setStyleSheet(make_stylesheet(red, radius=5))
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def disable(self):
        self.button.setEnabled(False)
        self.button.setText('')
        self.button.setCursor(QCursor(Qt.ForbiddenCursor))

    def enable(self, text=''):
        self.button.setEnabled(True)
        self.button.setText(text)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))

    def setText(self, text):
        self.button.setText(text)

    def getText(self):
        return self.button.text()

    def setStyle(self, style):
        self.button.setStyleSheet(style)

    def subscribe(self, func):
        self.button.clicked.connect(func)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)


class Atcrawl(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.setStyleSheet(make_color(light_grey))
        self.setWindowTitle("atCrawl Services")
        self.resize(500, 350)
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
        self.statusBrowser = StatusIndicator('Browser', 'offline', size=60)
        self.statusCrawler = StatusIndicator('Crawler', 'offline', size=60)
        self.statusGeneral = StatusIndicator(status='', size=self.width())
        self.statusGeneral.setStyle(make_stylesheet(grey))
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


class SplitFileEdit(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.button.subscribe(self.execute)
        self.can_process = False

    def setupUi(self):
        self.setStyleSheet(make_stylesheet(light_grey, radius=10))

        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.destination = FolderInput("Αποθήκευση αρχέιων στον φάκελο:",
                                       orientation=VERTICAL)
        self.splitRatio = IntInputParameter("Σπάσιμο αρχείου ανά:",
                                            orientation=VERTICAL)

        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='', size=self.width() - BTWIDTH)
        self.status.setStyle(make_stylesheet(grey))
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
            self.status.setStyle(make_stylesheet(grey))
        else:
            self.status.enable(text)
            self.status.setStyle(make_stylesheet(teal))

    def getParams(self):
        _params = {'filepath': self.fileToModify.getText(),
                   'destination': self.destination.getText(),
                   'k': self.splitRatio.getText()}

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
        self.setStyleSheet(make_stylesheet(light_grey, radius=10))

        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.fileToModify.setBrowseCallback(self.readInputFile)
        self.combosLayout = QHBoxLayout()
        self.colCombo1 = ComboInput("Στήλη ονόματος εικόνας")
        self.colCombo1.setOffset(100)
        self.colCombo2 = ComboInput("Στήλη URL εικόνας")
        self.colCombo2.setOffset(100)
        self.combosLayout.addWidget(self.colCombo1)
        self.combosLayout.addWidget(self.colCombo2)
        self.prefix = InputParameter("Link μπροστά από το όνομα της εικόνας:",
                                     orientation=VERTICAL)
        self.destination = FolderInput("Αποθήκευση αρχέιων στον φάκελο:",
                                       orientation=VERTICAL)

        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='', size=self.width() - BTWIDTH)
        self.status.setStyle(make_stylesheet(grey))
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
            self.status.setStyle(make_stylesheet(grey))
        else:
            self.status.enable(text)
            self.status.setStyle(make_stylesheet(teal))

    def getParams(self):
        _params = {'src': self.fileToModify.getText(),
                   'img_name': self.colCombo1.getCurrentText(),
                   'img_url': self.colCombo2.getCurrentText(),
                   'prefix': self.prefix.getText(),
                   'dst': self.destination.getText()}

        return _params

    def readInputFile(self):
        _file = self.fileToModify.getText()
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
        self.setStyleSheet(make_stylesheet(light_grey, radius=10))
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
        self.status = StatusIndicator(status='', size=self.width() - BTWIDTH)
        self.status.setStyle(make_stylesheet(grey))
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
            self.status.setStyle(make_stylesheet(grey))
        else:
            self.status.enable(text)
            self.status.setStyle(make_stylesheet(teal))

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
        self.setStyleSheet(make_stylesheet(light_grey, radius=10))
        self.source = FolderInput("Φάκελος αρχείων:",
                                  orientation=VERTICAL)
        self.colsLayout1 = QHBoxLayout()
        self.newColName1 = InputParameter("Νέα στήλη 1")
        self.newColName1.setOffset(80)
        self.newColName1.setPlaceholder("Προαιρετικό")
        self.newColValue1 = InputParameter("Τιμή στήλης 1")
        self.newColValue1.setOffset(80)
        self.newColValue1.setPlaceholder("Προαιρετικό")
        self.colsLayout1.addWidget(self.newColName1)
        self.colsLayout1.addWidget(self.newColValue1)
        self.destination = FileOutput("Αποθήκευση αρχείου:",
                                      orientation=VERTICAL)
        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='', size=self.width() - BTWIDTH)
        self.status.setStyle(make_stylesheet(grey))
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
            self.status.setStyle(make_stylesheet(grey))
        else:
            self.status.enable(text)
            self.status.setStyle(make_stylesheet(teal))

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
        self.setStyleSheet(make_stylesheet(light_grey, radius=10))

        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.fileToModify.setBrowseCallback(self.readInputFile)
        self.combosLayout = QHBoxLayout()
        self.colCombo1 = ComboInput("Στήλη εφαρμογής")
        self.colCombo1.setOffset(100)
        self.colCombo2 = ComboInput("Στήλη αλλαγών")
        self.colCombo2.setOffset(100)
        self.combosLayout.addWidget(self.colCombo1)
        self.combosLayout.addWidget(self.colCombo2)
        self.paramsLayout = QHBoxLayout()
        self.paramFilter = InputParameter("Φίλτρο:")
        self.paramFilter.setMinimumWidth(200)
        self.paramTrue = InputParameter("Τιμή για θετικές:")
        self.paramTrue.setMaximumWidth(50)
        self.paramFalse = InputParameter("Τιμή για αρνητικές:")
        self.paramFalse.setMaximumWidth(50)
        self.paramsLayout.addWidget(self.paramFilter)
        self.paramsLayout.addWidget(self.paramTrue)
        self.paramsLayout.addWidget(self.paramFalse)
        self.destination = FileOutput("Αποθήκευση αρχείου:",
                                      orientation=VERTICAL)

        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='', size=self.width() - BTWIDTH)
        self.status.setStyle(make_stylesheet(grey))
        self.button = Button("Εκτέλεση")
        self.buttonLayout.addWidget(self.status)
        self.buttonLayout.addWidget(self.button)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.fileToModify)
        self.pageLayout.addLayout(self.combosLayout)
        self.pageLayout.addLayout(self.paramsLayout)
        self.pageLayout.addWidget(self.destination)
        self.pageLayout.addStretch()
        self.pageLayout.addLayout(self.buttonLayout)
        self.setLayout(self.pageLayout)

    def mask_output(self, text=None):
        if text is None:
            self.status.disable()
            self.status.setStyle(make_stylesheet(grey))
        else:
            self.status.enable(text)
            self.status.setStyle(make_stylesheet(teal))

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
        self.setStyleSheet(make_stylesheet(grey, radius=10))

        self.fileToModify = FileInput("Αρχείο προς επεξεργασία:",
                                      orientation=VERTICAL)
        self.fileToModify.setBrowseCallback(self.readInputFile)
        self.colCombo1 = ComboInput("Στήλη εφαρμογής")

        self.destination = FileOutput("Αποθήκευση αρχείου:",
                                      orientation=VERTICAL)

        self.buttonLayout = QHBoxLayout()
        self.status = StatusIndicator(status='', size=self.width() - BTWIDTH)
        self.status.setStyle(make_stylesheet(grey))
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
            self.status.setStyle(make_stylesheet(grey))
        else:
            self.status.enable(text)
            self.status.setStyle(make_stylesheet(teal))

    def getParams(self):
        _params = {'src': self.fileToModify.getText(),
                   'col': self.colCombo1.getCurrentText(),
                   'dst': self.destination.getText()}

        return _params

    def readInputFile(self):
        _file = self.fileToModify.getText()
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


class EditWindow(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.setStyleSheet(make_color(light_grey))
        self.setWindowTitle("atCrawl Services")
        # self.resize(500, 300)
        self.layoutGeneral = QVBoxLayout()
        self.pageCombo = ComboInput('Διαδικασία',
                                    ["Ένωση αρχείων",
                                     "Αλλαγή τιμής σε στήλη",
                                     "Σορτάρισμα αρχείου",
                                     "Κατέβασμα εικόνων",
                                     "Δημιουργία εικόνων (Rellas)",
                                     "Κόψιμο αρχείου"])
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
        self.layoutGeneral.addWidget(self.pageCombo)
        self.layoutGeneral.addLayout(self.stackedLayout)
        self.setLayout(self.layoutGeneral)

    def switchPage(self):
        self.stackedLayout.setCurrentIndex(self.pageCombo.getCurrentIndex())


if __name__ == '__main__':
    app = QApplication([])
    volume = EditWindow()
    volume.show()
    app.exec_()

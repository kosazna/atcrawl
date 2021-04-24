# -*- coding: utf-8 -*-

from atcrawl.gui.colors import *
import os
from PyQt5.QtCore import QLine, QRegExp, Qt
from PyQt5.QtGui import QCursor, QFont, QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                             QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QToolButton, QVBoxLayout, QWidget)

HEIGHT = 25
HOFFSET = 55
BTWIDTH = 100
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
        self.lineEdit.setStyleSheet(make_stylesheet())
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        regexp = QRegExp('[^\.\<\>:\"/\\\|\?\*]*')
        validator = QRegExpValidator(regexp, self.lineEdit)
        self.lineEdit.setValidator(validator)
        self.setPlaceholder(placeholder)
        layout = QHBoxLayout()
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


class FolderInput(QWidget):
    def __init__(self,
                 label='',
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder)
        self.lastVisit = ''
        self.button.clicked.connect(self.browse)
        self.lineEdit.textChanged.connect(lambda x: self.pathExists(x))

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
        self.lineEdit.setStyleSheet(make_stylesheet())
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.setPlaceholder(placeholder)
        self.button = QToolButton()
        self.button.setFont(btFont)
        self.button.setFixedHeight(HEIGHT)
        self.button.setFixedWidth(HEIGHT)
        self.button.setText("...")
        self.button.setStyleSheet(make_stylesheet())
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def browse(self):
        file_path = QFileDialog.getExistingDirectory(directory=self.lastVisit)
        if file_path:
            self.lineEdit.setText(file_path)
            self.lastVisit = file_path

    def getText(self):
        return self.lineEdit.text()

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)

    def pathExists(self, path):
        if os.path.exists(path):
            self.lineEdit.setStyleSheet(make_stylesheet(border=green))
        else:
            self.lineEdit.setStyleSheet(make_stylesheet(border=red))


class FileInput(QWidget):
    def __init__(self,
                 label='',
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder)
        self.lastVisit = ''
        self.button.clicked.connect(self.browse)
        self.lineEdit.textChanged.connect(lambda x: self.pathExists(x))

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
        self.lineEdit.setStyleSheet(make_stylesheet())
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.setPlaceholder(placeholder)
        self.button = QToolButton()
        self.button.setFont(btFont)
        self.button.setFixedHeight(HEIGHT)
        self.button.setFixedWidth(HEIGHT)
        self.button.setText("...")
        self.button.setStyleSheet(make_stylesheet())
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def browse(self):
        filename = QFileDialog.getOpenFileName(directory=self.lastVisit)
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

    def pathExists(self, path):
        if os.path.exists(path):
            self.lineEdit.setStyleSheet(make_stylesheet(border=green))
        else:
            self.lineEdit.setStyleSheet(make_stylesheet(border=red))


class FileOutput(QWidget):
    def __init__(self,
                 label='',
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder)
        self.lastVisit = ''
        self.button.clicked.connect(self.browse)

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
        self.lineEdit.setStyleSheet(make_stylesheet())
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.setPlaceholder(placeholder)
        self.button = QToolButton()
        self.button.setFont(btFont)
        self.button.setFixedHeight(HEIGHT)
        self.button.setFixedWidth(HEIGHT)
        self.button.setText("...")
        self.button.setStyleSheet(make_stylesheet())
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit, 2)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def browse(self):
        filename = QFileDialog.getSaveFileName(directory=self.lastVisit)
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
        if completer is not None:
            _completer = QCompleter(completer)
            _completer.setCompletionMode(QCompleter.PopupCompletion)
            _completer.setCaseSensitivity(Qt.CaseInsensitive)
            _completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
            _completer.setFilterMode(Qt.MatchContains)
            _completer.popup().setStyleSheet(make_stylesheet(border=blue))
            self.lineEdit.setCompleter(_completer)

    def setupUi(self, label, orientation, hidden):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(labelFont)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.lineEdit = QLineEdit()
        self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet())
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
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
        self.lineEdit.setStyleSheet(make_stylesheet())
        self.lineEdit.setValidator(self.validator)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
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
        self.comboEdit.setStyleSheet(make_stylesheet())
        self.comboEdit.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        layout = QHBoxLayout()
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
        self.button.setStyleSheet(make_stylesheet(grey, radius=5))
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

    def setStyle(self, style):
        self.button.setStyleSheet(style)

    def subscribe(self, func):
        self.button.clicked.connect(func)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)


class CrawlerUI(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
 
    def setupUi(self):
        self.setStyleSheet(make_color(light_grey))
        self.setWindowTitle("atCrawl Services")
        # self.resize(550, 400)
        self.buttonLaunch = Button('launch')
        self.buttonCollect = Button('collect')
        self.buttonStop = Button('stop')
        self.buttonReset = Button('reset')
        self.buttonTerminate = Button('terminate')
        self.checkMeta = CheckInput('MetaCheck')
        self.inputUrl = InputParameter('URL')
        self.inputMeta0 = InputParameter('Meta0', completer=['ASTTOM', 'ASTOTA', 'DBOUND'])
        self.inputMeta0.setMinimumWidth(200)
        self.inputMeta1 = InputParameter('Meta1', hidden=True)
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


if __name__ == '__main__':
    app = QApplication([])
    volume = CrawlerUI()
    volume.show()
    app.exec_()

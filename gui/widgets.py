# -*- coding: utf-8 -*-


import os

from atcrawl.gui.colors import *
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QCursor, QFont, QIntValidator, QRegExpValidator, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                             QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QSizePolicy, QStackedLayout, QStyle,
                             QToolButton, QVBoxLayout, QWidget)

HORIZONTAL = 'H'
VERTICAL = 'V'
PATH_PLACEHOLDER = "Paste path here or browse..."


def get_dpi():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    screen = app.screens()[0]
    dpi = screen.physicalDotsPerInch()
    app.quit()

    return int(dpi)


if get_dpi() < 120:
    cssGuide = open(
        "D:/.temp/.dev/.aztool/atcrawl/gui/style_low_dpi.css").read()
else:
    cssGuide = open(
        "D:/.temp/.dev/.aztool/atcrawl/gui/style_high_dpi.css").read()


def show_popup(main_text, info='', icon=QMessageBox.Information):
    msg = QMessageBox()
    msg.setWindowTitle("atCrawl Dialog")
    msg.setText(main_text)
    msg.setIcon(icon)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.setInformativeText(info)
    msg.exec_()


class FileNameInput(QWidget):
    def __init__(self,
                 label='',
                 placeholder='',
                 parent=None,
                 size=('Small', 'Small'),
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, size)

    def setupUi(self, label, placeholder, size):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setObjectName(f"Label{size[0]}")
        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName(f"LineEdit{size[1]}")
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

    def setMaximumEditWidth(self, maxw):
        self.lineEdit.setMaximumWidth(maxw)

    def setMinimumEditWidth(self, minw):
        self.lineEdit.setMinimumWidth(minw)

    def setMaximumLabelWidth(self, maxw):
        self.label.setMaximumWidth(maxw)

    def setMinimumLabelWidth(self, minw):
        self.label.setMinimumWidth(minw)


class IOWidget(QWidget):
    lastVisit = ''
    ok = ("InputOk", "Path OK")
    warning = ("InputWarn", "Path Warning")
    error = ("InputError", "Path does not exist")

    def __init__(self,
                 label='',
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 orientation=HORIZONTAL,
                 size='Small',
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, orientation, size)
        self.button.clicked.connect(self.browse)
        self.lineEdit.textChanged.connect(lambda x: self.pathExists(x))
        self.browseCallback = None

    def setupUi(self, label, placeholder, orientation, size):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setObjectName(f"Label{size}")
        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName("InputDefault")
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setPlaceholder(placeholder)
        self.button = QToolButton()
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setText("2")
        self.button.setObjectName("Browse")
        if orientation == HORIZONTAL:
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

    @classmethod
    def setLastVisit(cls, folder):
        cls.lastVisit = folder

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

    def setMaximumEditWidth(self, maxw):
        self.lineEdit.setMaximumWidth(maxw)

    def setMinimumEditWidth(self, minw):
        self.lineEdit.setMinimumWidth(minw)

    def setMaximumLabelWidth(self, maxw):
        self.label.setMaximumWidth(maxw)

    def setMinimumLabelWidth(self, minw):
        self.label.setMinimumWidth(minw)

    def updateStyle(self, status):
        self.lineEdit.setObjectName(status)
        self.lineEdit.setStyleSheet(cssGuide)
        if status == self.ok[0]:
            self.lineEdit.setToolTip(self.ok[1])
        elif status == self.warning[0]:
            self.lineEdit.setToolTip(self.warning[1])
        elif status == self.error[0]:
            self.lineEdit.setToolTip(self.error[1])
        else:
            self.lineEdit.setToolTip("")

    def browse(self):
        pass

    def pathExists(self, path):
        pass


class FolderInput(IOWidget):
    warning = ("InputWarn", "Path should be a folder")

    def __init__(self,
                 label="",
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 orientation=HORIZONTAL,
                 size="Small",
                 *args,
                 **kwargs):
        super().__init__(label=label,
                         placeholder=placeholder,
                         parent=parent,
                         orientation=orientation,
                         size=size,
                         *args,
                         **kwargs)

    def browse(self):
        file_path = QFileDialog.getExistingDirectory(directory=self.lastVisit)
        if file_path:
            self.lineEdit.setText(file_path)
            IOWidget.setLastVisit(file_path)

            if self.browseCallback is not None:
                self.browseCallback()

    def pathExists(self, path):
        if path:
            if os.path.exists(path):
                if os.path.isdir(path):
                    self.updateStyle("InputOk")
                else:
                    self.updateStyle("InputWarn")
            else:
                self.updateStyle("InputError")
        else:
            self.updateStyle("InputDefault")


class FileInput(IOWidget):
    warning = ("InputWarn", "Path should be a folder")

    def __init__(self,
                 label="",
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 orientation=HORIZONTAL,
                 size="Small",
                 *args,
                 **kwargs):
        super().__init__(label=label,
                         placeholder=placeholder,
                         parent=parent,
                         orientation=orientation,
                         size=size,
                         *args,
                         **kwargs)

    def browse(self):
        filename = QFileDialog.getOpenFileName(directory=self.lastVisit)
        file_path = filename[0]
        if file_path:
            self.lineEdit.setText(file_path)
            IOWidget.setLastVisit(file_path)

            if self.browseCallback is not None:
                self.browseCallback()

    def pathExists(self, path):
        if path:
            if os.path.exists(path):
                if os.path.isfile(path):
                    self.updateStyle("InputOk")
                else:
                    self.updateStyle("InputWarn")
            else:
                self.updateStyle("InputError")
        else:
            self.updateStyle("InputDefault")


class FileOutput(IOWidget):
    def __init__(self,
                 label="",
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 orientation=HORIZONTAL,
                 size="Small",
                 *args,
                 **kwargs):
        super().__init__(label=label,
                         placeholder=placeholder,
                         parent=parent,
                         orientation=orientation,
                         size=size,
                         *args,
                         **kwargs)

    def browse(self):
        filename = QFileDialog.getSaveFileName(directory=self.lastVisit)
        file_path = filename[0]
        if file_path:
            self.lineEdit.setText(file_path)
            self.lastVisit = file_path


class InputParameter(QWidget):
    def __init__(self,
                 label='',
                 orientation=HORIZONTAL,
                 parent=None,
                 completer=None,
                 hidden=False,
                 size=("Small", "Small"),
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, orientation, hidden, size)
        self.setCompleter(completer)

    def setupUi(self, label, orientation, hidden, size):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setObjectName(f"Label{size[0]}")
        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName(f"LineEdit{size[1]}")
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        if hidden:
            self.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        if orientation == VERTICAL:
            layout = QVBoxLayout()
        else:
            layout = QHBoxLayout()
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

    def setMaximumEditWidth(self, maxw):
        self.lineEdit.setMaximumWidth(maxw)

    def setMinimumEditWidth(self, minw):
        self.lineEdit.setMinimumWidth(minw)

    def setMaximumLabelWidth(self, maxw):
        self.label.setMaximumWidth(maxw)

    def setMinimumLabelWidth(self, minw):
        self.label.setMinimumWidth(minw)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)

    def setCompleter(self, items):
        if items is not None:
            _completer = QCompleter(items)
            _completer.setCompletionMode(QCompleter.PopupCompletion)
            _completer.setCaseSensitivity(Qt.CaseInsensitive)
            _completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
            _completer.setFilterMode(Qt.MatchContains)
            _completer.popup().setObjectName("CompleterPopup")
            _completer.popup().setStyleSheet(cssGuide)
            self.lineEdit.setCompleter(_completer)


class IntInputParameter(QWidget):
    def __init__(self,
                 label='',
                 orientation=HORIZONTAL,
                 value_range=None,
                 parent=None,
                 size=("Small", "Small"),
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, orientation, value_range, size)

    def setupUi(self, label, orientation, value_range, size):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setObjectName(f"Label{size[0]}")
        self.validator = QIntValidator()
        if value_range is not None:
            self.validator.setRange(*value_range)
        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName(f"LineEdit{size[1]}")
        self.lineEdit.setValidator(self.validator)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        if orientation == VERTICAL:
            layout = QVBoxLayout()
        else:
            layout = QHBoxLayout()
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

    def setMaximumEditWidth(self, maxw):
        self.lineEdit.setMaximumWidth(maxw)

    def setMinimumEditWidth(self, minw):
        self.lineEdit.setMinimumWidth(minw)

    def setMaximumLabelWidth(self, maxw):
        self.label.setMaximumWidth(maxw)

    def setMinimumLabelWidth(self, minw):
        self.label.setMinimumWidth(minw)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)


class ComboInput(QWidget):
    def __init__(self,
                 label='',
                 items=None,
                 parent=None,
                 size='Small',
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, items, size)

    def setupUi(self, label, items, size):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setObjectName(f"Label{size}")
        self.comboEdit = QComboBox()
        self.comboEdit.setObjectName("Combo")
        self.comboEdit.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents)
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.comboEdit, 1, alignment=Qt.AlignLeft)
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

    def setMaximumLabelWidth(self, maxw):
        self.label.setMaximumWidth(maxw)

    def setMinimumLabelWidth(self, minw):
        self.label.setMinimumWidth(minw)


class CheckInput(QCheckBox):
    def __init__(self, label='', checked=True, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, checked)

    def setupUi(self, label, checked):
        self.setText(label)
        self.setObjectName("Check")
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
        self.setObjectName("BlueButton")
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def disable(self):
        self.setEnabled(False)
        self.setStyle(f"GreyButton")
        self.setCursor(QCursor(Qt.ForbiddenCursor))

    def enable(self, color):
        self.setEnabled(True)
        self.setStyle(f"{color.name.capitalize()}Button")
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def subscribe(self, func):
        self.clicked.connect(func)

    def setStyle(self, object_name):
        self.setObjectName(object_name)
        self.setStyleSheet(cssGuide)


class StatusIndicator(QWidget):
    def __init__(self,
                 label='',
                 status='',
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, status)

    def setupUi(self, label, status):
        layout = QHBoxLayout()
        self.button = QToolButton()
        self.button.setText(status)
        self.button.setEnabled(False)
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if label:
            self.label = QLabel()
            self.label.setText(label)
            self.label.setObjectName("LabelSmall")
            layout.addWidget(self.label)
            self.button.setObjectName("StatusSmallOffline")
            layout.addWidget(self.button, 1, alignment=Qt.AlignLeft)
            self.has_label = True
        else:
            self.button.setObjectName("StatusBigDisabled")
            layout.addWidget(self.button)
            self.has_label = False

        self.setLayout(layout)

    def disable(self, text=''):
        self.button.setEnabled(False)
        self.setText(text)
        if self.has_label:
            self.setStyle(f"StatusSmall{text.capitalize()}")
        else:
            self.setStyle("StatusBigDisabled")

    def enable(self, text=''):
        self.button.setEnabled(True)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.setText(text)
        if self.has_label:
            self.setStyle(f"StatusSmall{text.capitalize()}")
        else:
            self.setStyle("StatusBigEnabled")

    def setText(self, text):
        self.button.setText(text)

    def getText(self):
        return self.button.text()

    def setStyle(self, object_name):
        self.button.setObjectName(object_name)
        self.button.setStyleSheet(cssGuide)

    def subscribe(self, func):
        self.button.clicked.connect(func)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)


class Dummy(QWidget):
    def __init__(self,
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWidget")
        self.setStyleSheet(cssGuide)
        self.layout = QVBoxLayout()
        self.layoutTop = QHBoxLayout()
        self.layoutGeneral = QVBoxLayout()
        self.layoutButtons = QVBoxLayout()
        self.layoutComboCheck = QHBoxLayout()
        self.folderInput = FolderInput("Folder", parent=self, size='Small')
        self.fileInput = FileInput("File In", parent=self, size='Small')
        self.fileOutput = FileOutput("File Out", parent=self, size='Small')
        self.filename = FileNameInput(
            "Filename", parent=self, size=('Small', 'Big'))
        self.input = InputParameter(
            "Input", parent=self, completer=['Astota', 'Asttom'], size=('Small', 'Big'))
        self.inputInt = IntInputParameter("Int", parent=self)
        self.combo = ComboInput("Combo", items=["1", "2", "3"], parent=self)
        self.check = CheckInput("Check", parent=self)
        self.status = StatusIndicator(parent=self)
        self.statusSmall = StatusIndicator(
            label='Status', status='offline', parent=self)
        self.button1 = Button("accept", parent=self)
        self.button2 = Button("decline", parent=self)
        self.button3 = Button("process", parent=self)

        self.layoutGeneral.addWidget(self.folderInput)
        self.layoutGeneral.addWidget(self.fileInput)
        self.layoutGeneral.addWidget(self.fileOutput)
        self.layoutGeneral.addWidget(self.filename)
        self.layoutGeneral.addWidget(self.input)
        self.layoutGeneral.addWidget(self.inputInt)

        self.layoutComboCheck.addWidget(self.combo)
        self.layoutComboCheck.addWidget(self.check)
        self.layoutGeneral.addLayout(self.layoutComboCheck)
        self.layoutGeneral.addWidget(self.statusSmall)

        self.layoutButtons.addWidget(self.button1)
        self.layoutButtons.addWidget(self.button2)
        self.layoutButtons.addWidget(self.button3)

        self.layoutTop.addLayout(self.layoutGeneral)
        self.layoutTop.addLayout(self.layoutButtons)

        self.layout.addLayout(self.layoutTop)
        self.layout.addWidget(self.status)

        self.setLayout(self.layout)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = Dummy()
    ui.show()
    sys.exit(app.exec_())

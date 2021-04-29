# -*- coding: utf-8 -*-


import os

from atcrawl.gui.colors import *
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QCursor, QFont, QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                             QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QSizePolicy, QStackedLayout, QStyle,
                             QToolButton, QVBoxLayout, QWidget)

HEIGHT = 25
HOFFSET = 55
BTWIDTH = 80
# FONTSIZE = 10
# FONT = "Segoe UI"
HORIZONTAL = 'H'
VERTICAL = 'V'
PATH_PLACEHOLDER = "Paste path here or browse..."

# labelFont = QFont(FONT, FONTSIZE)
# btFont = QFont(FONT, FONTSIZE)
# btFont.setBold(True)

stylesheet = open("D:/.temp/.dev/.aztool/atcrawl/gui/style.css").read()

visuals = {
    'widget_height': 25,
    'line_offset': 55,
    'button_width': 80,
    'font': "Segoe UI",
    'fontsize': 10,
    'label': '',
    'path_placeholder': "Paste path here or browse...",
    'orientation': HORIZONTAL,
    'completer': None,
    'hidden': False,
    'value_range': None,
    'checked': True,
    'combo_items': None,
    'status': '',
    'status_size': 250,
    'base_folder': ''
}


def show_popup(main_text, info='', icon=QMessageBox.Information):
    msg = QMessageBox()
    # msg.setFont(labelFont)
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
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder)

    def setupUi(self, label, placeholder):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        # self.label.setFont(labelFont)
        self.label.setMinimumWidth(HOFFSET)
        self.label.setObjectName("Label")
        self.lineEdit = QLineEdit()
        # self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setObjectName("LineEdit")
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
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, orientation)
        self.button.clicked.connect(self.browse)
        self.lineEdit.textChanged.connect(lambda x: self.pathExists(x))
        self.browseCallback = None

    def setupUi(self, label, placeholder, orientation):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setObjectName("Label")
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
        self.lineEdit.setStyleSheet(stylesheet)
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

    def __init__(self, label="", placeholder=PATH_PLACEHOLDER, parent=None, orientation=HORIZONTAL, *args, **kwargs):
        super().__init__(label=label, placeholder=placeholder,
                         parent=parent, orientation=orientation, *args, **kwargs)

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

    def __init__(self, label="", placeholder=PATH_PLACEHOLDER, parent=None, orientation=HORIZONTAL, *args, **kwargs):
        super().__init__(label=label, placeholder=placeholder,
                         parent=parent, orientation=orientation, *args, **kwargs)

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
    def __init__(self, label="", placeholder=PATH_PLACEHOLDER, parent=None, orientation=HORIZONTAL, *args, **kwargs):
        super().__init__(label=label, placeholder=placeholder,
                         parent=parent, orientation=orientation, *args, **kwargs)

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
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, orientation, hidden)
        self.setCompleter(completer)

    def setupUi(self, label, orientation, hidden):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        # self.label.setFont(labelFont)
        self.label.setObjectName("Label")
        self.lineEdit = QLineEdit()
        # self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setObjectName("LineEdit")
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
        # self.label.setFont(labelFont)
        self.label.setObjectName("Label")
        self.validator = QIntValidator()
        if value_range is not None:
            self.validator.setRange(*value_range)
        self.lineEdit = QLineEdit()
        # self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setObjectName("LineEdit")
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
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, items)

    def setupUi(self, label, items):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        # self.label.setFont(labelFont)
        self.label.setObjectName("Label")
        self.label.setMinimumWidth(HOFFSET)
        self.comboEdit = QComboBox()
        # self.comboEdit.setFont(labelFont)
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
        self.setFixedHeight(HEIGHT)
        # self.setFont(labelFont)
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
        self.setObjectName("Button")
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
            # self.label.setFont(labelFont)
            self.label.setText(label)
            self.label.setObjectName("Label")
            self.label.setFixedHeight(HEIGHT)
            self.label.setFixedWidth(HOFFSET)
            layout.addWidget(self.label)
        self.button = QToolButton()
        # self.button.setFont(btFont)
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


class Dummy(QWidget):
    def __init__(self,
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWidget")
        self.setStyleSheet(stylesheet)
        self.layout = QVBoxLayout()
        self.layoutTop = QHBoxLayout()
        self.layoutGeneral = QVBoxLayout()
        self.layoutButtons = QVBoxLayout()
        self.folderInput = FolderInput("Folder", parent=self)
        self.fileInput = FileInput("File In", parent=self)
        self.fileOutput = FileOutput("File Out", parent=self)
        self.input = InputParameter("Input", parent=self)
        self.inputInt = IntInputParameter("Int", parent=self)
        self.combo = ComboInput("Combo", items=["1", "2", "3"], parent=self)
        self.status = StatusIndicator(size=self.width(), parent=self)
        self.button1 = Button("accept", parent=self)
        self.button2 = Button("decline", parent=self)
        self.button3 = Button("process", parent=self)

        self.status.setStyle(make_stylesheet(dark, foreground=teal))

        self.layoutGeneral.addWidget(self.folderInput)
        self.layoutGeneral.addWidget(self.fileInput)
        self.layoutGeneral.addWidget(self.fileOutput)
        self.layoutGeneral.addWidget(self.input)
        self.layoutGeneral.addWidget(self.inputInt)
        self.layoutGeneral.addWidget(self.combo)

        self.layoutButtons.addWidget(self.button1)
        self.layoutButtons.addWidget(self.button2)
        self.layoutButtons.addWidget(self.button3)

        self.layoutTop.addLayout(self.layoutGeneral)
        self.layoutTop.addLayout(self.layoutButtons)

        self.layout.addLayout(self.layoutTop)
        self.layout.addWidget(self.status)        

        self.setLayout(self.layout)


class MyLineEdit(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)

        self.setPlaceholderText(self.tr('Password'))
        self.setEchoMode(QLineEdit.Password)

        self.btnToggle = QToolButton(self)
        self.btnToggle.setFont(QFont("Webdings", 20))
        self.btnToggle.setText('a')
        self.btnToggle.setCursor(Qt.ArrowCursor)
        self.btnToggle.setStyleSheet('QToolButton { border: none; padding: 0px; }')

        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.setStyleSheet('QLineEdit {{ padding-right: {}px; }} '.format(self.btnToggle.sizeHint().width() + frameWidth + 1))
        msz = self.minimumSizeHint()
        self.setMinimumSize(max(msz.width(), self.btnToggle.sizeHint().height() + frameWidth * 2 + 2),
                            max(msz.height(), self.btnToggle.sizeHint().height() + frameWidth * 2 + 2))

    def resizeEvent(self, event):
        sz = self.btnToggle.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.btnToggle.move(self.rect().right() - frameWidth - sz.width(),
                           (self.rect().bottom() + 1 - sz.height())/2)



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = Dummy()
    ui.show()
    sys.exit(app.exec_())

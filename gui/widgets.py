# -*- coding: utf-8 -*-


import os

from atcrawl.gui.colors import *
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QCursor, QFont, QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                             QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QSizePolicy, QStackedLayout,
                             QToolButton, QVBoxLayout, QWidget)

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

visuals = {
    'widget_height': 25,
    'line_offset': 55,
    'button_width': 80,
    'font': "Segoe UI",
    'fontsize': 10,
    'label' : '',
    'path_placeholder': "Paste path here or browse...",
    'orientation': HORIZONTAL,
    'completer': None,
    'hidden': False,
    'value_range': None,
    'checked': True,
    'combo_items': None,
    'status': '',
    'status_size': 250
}

def show_popup(main_text, info='', icon=QMessageBox.Information):
    msg = QMessageBox()
    msg.setFont(labelFont)
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
                 first_visit = '',
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, orientation)
        self.lastVisit = first_visit
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
                 first_visit = '',
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, orientation)
        self.lastVisit = first_visit
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
                 first_visit = '',
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, orientation)
        self.lastVisit = first_visit
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
        self.setStyleSheet(make_stylesheet(blue))
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


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = FileInput()
    ui.show()
    sys.exit(app.exec_())

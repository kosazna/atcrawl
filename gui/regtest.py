from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication,
                             QDialogButtonBox)
from atcrawl.gui.colors import *

HEIGHT = 25
HOFFSET = 60
FONTSIZE = 10
FONT = "Segoe UI"


class FileNameInput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 *args,
                 **kwargs):
        super(FileNameInput, self).__init__(*args, **kwargs)
        self.setupUI(label)

    def setupUI(self, label):
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
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)


class FolderInput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 *args,
                 **kwargs):
        super(FolderInput, self).__init__(*args, **kwargs)
        self.setupUI(label)
        self.lastVisit = ''
        self.button.clicked.connect(self.browse)

    def setupUI(self, label):
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


class FileInput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 *args,
                 **kwargs):
        super(FileInput, self).__init__(*args, **kwargs)
        self.setupUI(label)
        self.lastVisit = ''
        self.button.clicked.connect(self.browse)

    def setupUI(self, label):
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


class FileOutput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 *args,
                 **kwargs):
        super(FileOutput, self).__init__(*args, **kwargs)
        self.setupUI(label)
        self.lastVisit = ''
        self.button.clicked.connect(self.browse)

    def setupUI(self, label):
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


class InputParameter(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 orientation='vertical',
                 *args,
                 **kwargs):
        super(InputParameter, self).__init__(*args, **kwargs)
        self.setupUI(label, orientation)

    def setupUI(self, label, orientation):
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
        if orientation == 'vertical':
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


class IntInputParameter(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 orientation='vertical',
                 value_range=None,
                 *args,
                 **kwargs):
        super(IntInputParameter, self).__init__(*args, **kwargs)
        self.setupUI(label, orientation, value_range)

    def setupUI(self, label, orientation, value_range):
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
        if orientation == 'vertical':
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


class ComboInput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 items=None,
                 *args,
                 **kwargs):
        super(ComboInput, self).__init__(*args, **kwargs)
        self.setupUI(label, items)

    def setupUI(self, label, items):
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

    def currentText(self):
        return self.comboEdit.currentText()


class CheckInput(QtWidgets.QCheckBox):
    def __init__(self, label='', checked=True, *args, **kwargs):
        super(CheckInput, self).__init__(*args, **kwargs)
        self.setupUI(label, checked)

    def setupUI(self, label, checked):
        font = QtGui.QFont()
        font.setFamily(FONT)
        font.setPointSize(FONTSIZE)
        self.setText(label)
        self.setFixedHeight(HEIGHT)
        self.setFont(font)
        self.setChecked(checked)
        self.animateClick(100)
        # self.setStyleSheet(make_color(white, 0))

    def enable(self):
        self.setEnabled(True)

    def disable(self):
        self.setEnabled(False)


class StatusIndicator(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 status='',
                 size=100,
                 *args,
                 **kwargs):
        super(StatusIndicator, self).__init__(*args, **kwargs)
        self.setupUI(label, status, size)

    def setupUI(self, label, status, size):
        labelFont = QtGui.QFont()
        labelFont.setFamily(FONT)
        labelFont.setPointSize(FONTSIZE)
        btFont = QtGui.QFont()
        btFont.setFamily(FONT)
        btFont.setPointSize(FONTSIZE)
        btFont.setBold(True)
        self.label = QtWidgets.QLabel()
        self.label.setFont(labelFont)
        self.label.setText(label)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.label.setFixedHeight(HEIGHT)
        self.label.setFixedWidth(HOFFSET)
        self.button = QtWidgets.QToolButton()
        self.button.setFont(btFont)
        self.button.setText(status)
        self.button.setFixedHeight(HEIGHT)
        self.button.setMinimumWidth(size)
        self.button.setEnabled(False)
        self.button.setStyleSheet(make_stylesheet(grey, radius=5))
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def disable(self):
        self.button.setEnabled(False)

    def enable(self):
        self.button.setEnabled(True)

    def setText(self, text):
        self.button.setText(text)

    def style(self, style):
        self.button.setStyleSheet(style)


class MainApp(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)
        self.setStyleSheet(make_color(light_grey, 0.9))
        self.resize(800, 600)
        layout = QtWidgets.QHBoxLayout()

        left = QtWidgets.QVBoxLayout()
        right = QtWidgets.QVBoxLayout()

        self.l5 = InputParameter('URL', 'horizontal')
        self.l1 = InputParameter('Meta Title SEO')
        self.l7 = IntInputParameter('Discount', 'horizontal')
        self.l2 = FileNameInput('Filename')
        self.l3 = FileInput('Import')
        self.l4 = FileOutput('Save to')
        self.l6 = StatusIndicator('Browser', 'offline')
        self.l8 = StatusIndicator('Crawler', 'offline')
        self.l9 = FolderInput('Folder')
        self.l10 = ComboInput('Process', ['Cavino', 'Concepts', 'Giochi'])
        self.l11 = CheckInput('Export')
        left.addWidget(self.l5)
        left.addWidget(self.l1)
        left.addWidget(self.l7)
        left.addWidget(self.l2)
        left.addWidget(self.l3)
        left.addWidget(self.l4)
        left.addWidget(self.l9)
        left.addWidget(self.l10)
        left.addStretch()

        right.addWidget(self.l6)
        right.addWidget(self.l8)
        right.addWidget(self.l11)
        right.addStretch()

        layout.addLayout(left)
        layout.addLayout(right)

        self.setLayout(layout)


app = QtWidgets.QApplication([])
app.setStyle('Fusion')
volume = MainApp()
volume.show()
app.exec_()

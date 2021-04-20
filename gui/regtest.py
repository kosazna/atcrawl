from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication,
                             QDialogButtonBox)
from atcrawl.gui.colors import *

HEIGHT = 30
HOFFSET = 80
BTWIDTH = 100
FONTSIZE = 10
FONT = "Segoe UI"


class FileNameInput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 *args,
                 **kwargs):
        super(FileNameInput, self).__init__(*args, **kwargs)
        self.setupUi(label)

    def setupUi(self, label):
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

    def getText(self):
        return self.lineEdit.text()


class FolderInput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 *args,
                 **kwargs):
        super(FolderInput, self).__init__(*args, **kwargs)
        self.setupUi(label)
        self.lastVisit = ''
        self.button.clicked.connect(self.browse)

    def setupUi(self, label):
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

    def getText(self):
        return self.lineEdit.text()


class FileInput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 *args,
                 **kwargs):
        super(FileInput, self).__init__(*args, **kwargs)
        self.setupUi(label)
        self.lastVisit = ''
        self.button.clicked.connect(self.browse)

    def setupUi(self, label):
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

    def getText(self):
        return self.lineEdit.text()


class FileOutput(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 *args,
                 **kwargs):
        super(FileOutput, self).__init__(*args, **kwargs)
        self.setupUi(label)
        self.lastVisit = ''
        self.button.clicked.connect(self.browse)

    def setupUi(self, label):
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

    def getText(self):
        return self.lineEdit.text()


class InputParameter(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 orientation='vertical',
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

    def getText(self):
        return self.lineEdit.text()


class IntInputParameter(QtWidgets.QWidget):
    def __init__(self,
                 label='',
                 orientation='vertical',
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

    def getText(self):
        return self.lineEdit.text()


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

    def enable(self):
        self.setEnabled(True)

    def disable(self):
        self.setEnabled(False)

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
        self.setStyleSheet(make_stylesheet(blue))
        self.setMinimumWidth(BTWIDTH)

    def disable(self):
        self.setEnabled(False)
        self.setStyleSheet(make_stylesheet(grey))

    def enable(self, color):
        self.setEnabled(True)
        self.setStyleSheet(make_stylesheet(color))

    def subscribe(self, func):
        self.clicked.connect(func)


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

    def enable(self):
        self.button.setEnabled(True)

    def setText(self, text):
        self.button.setText(text)

    def setStyle(self, style):
        self.button.setStyleSheet(style)

    def subscribe(self, func):
        self.button.clicked.connect(func)


class MainApp(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)
        self.setStyleSheet(make_color(light_grey))
        self.resize(800, 500)
        whole = QtWidgets.QVBoxLayout()
        top = QtWidgets.QVBoxLayout()
        bottom = QtWidgets.QHBoxLayout()

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
        self.l12 = Button('Collect')
        self.l13 = Button('Reset')
        self.l14 = StatusIndicator(status='kostas', size=self.width())
 
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
        right.addWidget(self.l11, alignment=QtCore.Qt.AlignRight)
        right.addStretch(1)
        right.addWidget(self.l12, alignment=QtCore.Qt.AlignRight)
        right.addWidget(self.l13, alignment=QtCore.Qt.AlignRight)
        right.addStretch()

        top.addWidget(self.l5)
        top.addWidget(self.l14)
        bottom.addLayout(left)
        bottom.addLayout(right)

        whole.addLayout(top)
        whole.addLayout(bottom)

        self.setLayout(whole)


app = QtWidgets.QApplication([])
# app.setStyle('Fusion')
volume = MainApp()
volume.show()
app.exec_()

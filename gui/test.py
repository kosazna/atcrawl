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
FONTSIZE = 10
FONT = "Segoe UI"
HORIZONTAL = 'H'
VERTICAL = 'V'
PATH_PLACEHOLDER = "Paste path here or browse..."

labelFont = QFont(FONT, FONTSIZE)
btFont = QFont(FONT, FONTSIZE)
btFont.setBold(True)

stylesheet = open("D:/.temp/.dev/.aztool/atcrawl/gui/style.css").read()


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
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(labelFont)
        self.lineEdit = QLineEdit()
        self.lineEdit.setFont(labelFont)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setObjectName("InputDefault")
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setPlaceholder(placeholder)
        self.button = QToolButton()
        self.button.setFont(btFont)
        self.button.setFixedHeight(HEIGHT)
        self.button.setFixedWidth(HEIGHT)
        self.button.setText("...")
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
            self.lastVisit = file_path

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
            self.lastVisit = file_path

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

        self.folderInput = FolderInput("Folder", parent=self)
        self.folderInput.setObjectName("FolderInput")
        self.fileInput = FileInput("File In", parent=self)
        self.fileOutput = FileOutput("File Out", parent=self)
        IOWidget.setLastVisit("C:/Users/aznavouridis.k/Desktop/Terpos")

        self.layout.addWidget(self.folderInput)
        self.layout.addWidget(self.fileInput)
        self.layout.addWidget(self.fileOutput)


        self.setLayout(self.layout)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = Dummy()
    ui.show()
    sys.exit(app.exec_())

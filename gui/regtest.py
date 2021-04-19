from PyQt5 import QtCore, QtGui, QtWidgets
from atcrawl.gui.colors import *

HEIGHT = 25
HOFFSET = 60
FONTSIZE = 10


class FileNameInput(QtWidgets.QWidget):
    def __init__(self, label='', *args, **kwargs):
        super(FileNameInput, self).__init__(*args, **kwargs)

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(FONTSIZE)

        layout = QtWidgets.QHBoxLayout()

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

        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)


class FileInput(QtWidgets.QWidget):
    def __init__(self, label='', *args, **kwargs):
        super(FileInput, self).__init__(*args, **kwargs)

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(FONTSIZE)

        layout = QtWidgets.QHBoxLayout()

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

        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.lastVisit = ''

        self.button.clicked.connect(self.browse)

    def browse(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            directory=self.lastVisit)
        file_path = filename[0]
        if file_path:
            self.lineEdit.setText(file_path)
            self.lastVisit = file_path


class FileOutput(QtWidgets.QWidget):
    def __init__(self, label='', *args, **kwargs):
        super(FileOutput, self).__init__(*args, **kwargs)

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(FONTSIZE)

        layout = QtWidgets.QHBoxLayout()

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

        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.lastVisit = ''

        self.button.clicked.connect(self.browse)

    def browse(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(
            directory=self.lastVisit)
        file_path = filename[0]
        if file_path:
            self.lineEdit.setText(file_path)
            self.lastVisit = file_path


class ParameterInput(QtWidgets.QWidget):
    def __init__(self, label='', orientation='vertical', *args, **kwargs):
        super(ParameterInput, self).__init__(*args, **kwargs)

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(FONTSIZE)

        self.label = QtWidgets.QLabel()
        self.label.setText(label)
        self.label.setFixedHeight(HEIGHT)
        self.label.setFont(font)
        self.label.setStyleSheet(make_stylesheet(alpha=0))

        if orientation == 'horizontal':
            self.label.setMinimumWidth(HOFFSET)

        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setFont(font)
        self.lineEdit.setFixedHeight(HEIGHT)
        self.lineEdit.setStyleSheet(make_stylesheet())

        if orientation == 'vertical':
            layout = QtWidgets.QVBoxLayout()
        else:
            layout = QtWidgets.QHBoxLayout()

        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)


class StatusIndicator(QtWidgets.QWidget):
    def __init__(self, label='', *args, **kwargs):
        super(StatusIndicator, self).__init__(*args, **kwargs)

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(FONTSIZE)

        self.label = QtWidgets.QLabel()
        self.label.setFont(font)
        self.label.setText(label)
        self.label.setStyleSheet(make_stylesheet(alpha=0))
        self.label.setFixedHeight(HEIGHT)
        self.label.setFixedWidth(HOFFSET)

        font.setBold(True)
        self.status = QtWidgets.QLineEdit()
        self.status.setFont(font)
        self.status.setText('label')
        self.status.setFixedHeight(HEIGHT)
        self.status.setEnabled(False)
        self.status.setStyleSheet(make_stylesheet(grey, radius=8))
        self.status.setAlignment(QtCore.Qt.AlignCenter)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.status)
        self.setLayout(layout)


class MainApp(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)
        self.setStyleSheet(make_color(light_grey, 0.9))
        layout = QtWidgets.QVBoxLayout()

        self.l5 = ParameterInput('URL', 'horizontal')
        self.l1 = ParameterInput('Meta Title SEO')
        self.l2 = FileNameInput('Filename')
        self.l3 = FileInput('Import')
        self.l4 = FileOutput('Save to')
        self.l6 = StatusIndicator('Status')
        layout.addWidget(self.l5)
        layout.addWidget(self.l1)
        layout.addWidget(self.l2)
        layout.addWidget(self.l3)
        layout.addWidget(self.l4)
        layout.addWidget(self.l6)
        self.setLayout(layout)


app = QtWidgets.QApplication([])
volume = MainApp()
volume.show()
app.exec_()

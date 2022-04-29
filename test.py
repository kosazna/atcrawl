# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'progess_barwUidno.ui'
##
# Created by: Qt User Interface Compiler version 5.15.2
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Frame(QWidget):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(620, 52)
        Frame.setStyleSheet(u"#ProgressBar {\n"
                            "  font-family: \"Segoe UI\";\n"
                            "  border: 1px solid #212529;\n"
                            "  background-color: transparent;\n"
                            "  border-radius: 3px;\n"
                            "  font: 12px;\n"
                            "  font-weight: bold;\n"
                            "  max-height: 20px;\n"
                            "  min-height: 20px;\n"
                            "  min-width: 150px;\n"
                            "}\n"
                            "\n"
                            "#ProgressBar::chunk {\n"
                            "  background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(98, 116, 157, 255), stop:0.5 rgba(89, 135, 120, 255), stop:1 rgba(91, 192, 100, 255));\n"
                            "}")
        self.horizontalLayout = QHBoxLayout(Frame)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 2, 4, 2)
        self.ProgressBar = QProgressBar(Frame)
        self.ProgressBar.setObjectName(u"ProgressBar")
        self.ProgressBar.setValue(70)
        self.ProgressBar.setAlignment(Qt.AlignCenter)
        self.ProgressBar.setTextVisible(True)
        self.ProgressBar.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.ProgressBar)

        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(
            QCoreApplication.translate("Frame", u"Frame", None))
    # retranslateUi

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    frame = QFrame()
    volume = Ui_Frame()
    volume.setupUi(frame)
    volume.show()
    sys.exit(app.exec_())

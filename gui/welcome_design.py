# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'atcrawl_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WelcomeUI(object):
    def setupUi(self, WelcomeUI):
        WelcomeUI.setObjectName("WelcomeUI")
        WelcomeUI.resize(378, 530)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/layers/static/main_layer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        WelcomeUI.setWindowIcon(icon)
        WelcomeUI.setStyleSheet("background-color: rgb(101, 104, 114);")
        self.centralwidget = QtWidgets.QWidget(WelcomeUI)
        self.centralwidget.setObjectName("centralwidget")
        self.bt_skroutz = QtWidgets.QToolButton(self.centralwidget)
        self.bt_skroutz.setEnabled(True)
        self.bt_skroutz.setGeometry(QtCore.QRect(80, 130, 221, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.bt_skroutz.setFont(font)
        self.bt_skroutz.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(13, 5, 81, 255), stop:1 rgba(36, 176, 189, 255));\n"
"color: rgb(255, 255, 255);\n"
"border-width:10px;\n"
"border-radius:20px;\n"
"")
        self.bt_skroutz.setCheckable(False)
        self.bt_skroutz.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.bt_skroutz.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.bt_skroutz.setAutoRaise(True)
        self.bt_skroutz.setArrowType(QtCore.Qt.NoArrow)
        self.bt_skroutz.setObjectName("bt_skroutz")
        self.bt_antallaktika = QtWidgets.QToolButton(self.centralwidget)
        self.bt_antallaktika.setEnabled(True)
        self.bt_antallaktika.setGeometry(QtCore.QRect(80, 70, 220, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.bt_antallaktika.setFont(font)
        self.bt_antallaktika.setToolTip("")
        self.bt_antallaktika.setWhatsThis("")
        self.bt_antallaktika.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.bt_antallaktika.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(13, 5, 81, 255), stop:1 rgba(36, 176, 189, 255));\n"
"color: rgb(255, 255, 255);\n"
"border-width:10px;\n"
"border-radius:20px;\n"
"")
        self.bt_antallaktika.setCheckable(False)
        self.bt_antallaktika.setAutoRepeatDelay(-3)
        self.bt_antallaktika.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.bt_antallaktika.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.bt_antallaktika.setAutoRaise(True)
        self.bt_antallaktika.setArrowType(QtCore.Qt.NoArrow)
        self.bt_antallaktika.setObjectName("bt_antallaktika")
        self.bt_tripadvisor = QtWidgets.QToolButton(self.centralwidget)
        self.bt_tripadvisor.setEnabled(True)
        self.bt_tripadvisor.setGeometry(QtCore.QRect(80, 310, 221, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.bt_tripadvisor.setFont(font)
        self.bt_tripadvisor.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(13, 5, 81, 255), stop:1 rgba(36, 176, 189, 255));\n"
"color: rgb(255, 255, 255);\n"
"border-width:10px;\n"
"border-radius:20px;\n"
"")
        self.bt_tripadvisor.setCheckable(False)
        self.bt_tripadvisor.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.bt_tripadvisor.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.bt_tripadvisor.setAutoRaise(True)
        self.bt_tripadvisor.setArrowType(QtCore.Qt.NoArrow)
        self.bt_tripadvisor.setObjectName("bt_tripadvisor")
        self.header = QtWidgets.QTextBrowser(self.centralwidget)
        self.header.setGeometry(QtCore.QRect(10, 0, 361, 61))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.header.setFrameShadow(QtWidgets.QFrame.Plain)
        self.header.setObjectName("header")
        self.bt_spitogatos = QtWidgets.QToolButton(self.centralwidget)
        self.bt_spitogatos.setEnabled(True)
        self.bt_spitogatos.setGeometry(QtCore.QRect(80, 430, 221, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.bt_spitogatos.setFont(font)
        self.bt_spitogatos.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(13, 5, 81, 255), stop:1 rgba(36, 176, 189, 255));\n"
"color: rgb(255, 255, 255);\n"
"border-width:10px;\n"
"border-radius:20px;\n"
"")
        self.bt_spitogatos.setCheckable(False)
        self.bt_spitogatos.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.bt_spitogatos.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.bt_spitogatos.setAutoRaise(True)
        self.bt_spitogatos.setArrowType(QtCore.Qt.NoArrow)
        self.bt_spitogatos.setObjectName("bt_spitogatos")
        self.bt_booking = QtWidgets.QToolButton(self.centralwidget)
        self.bt_booking.setEnabled(True)
        self.bt_booking.setGeometry(QtCore.QRect(80, 370, 221, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.bt_booking.setFont(font)
        self.bt_booking.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(13, 5, 81, 255), stop:1 rgba(36, 176, 189, 255));\n"
"color: rgb(255, 255, 255);\n"
"border-width:10px;\n"
"border-radius:20px;\n"
"")
        self.bt_booking.setCheckable(False)
        self.bt_booking.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.bt_booking.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.bt_booking.setAutoRaise(True)
        self.bt_booking.setArrowType(QtCore.Qt.NoArrow)
        self.bt_booking.setObjectName("bt_booking")
        self.bt_rellas = QtWidgets.QToolButton(self.centralwidget)
        self.bt_rellas.setEnabled(True)
        self.bt_rellas.setGeometry(QtCore.QRect(80, 190, 221, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.bt_rellas.setFont(font)
        self.bt_rellas.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(13, 5, 81, 255), stop:1 rgba(36, 176, 189, 255));\n"
"color: rgb(255, 255, 255);\n"
"border-width:10px;\n"
"border-radius:20px;\n"
"")
        self.bt_rellas.setCheckable(False)
        self.bt_rellas.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.bt_rellas.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.bt_rellas.setAutoRaise(True)
        self.bt_rellas.setArrowType(QtCore.Qt.NoArrow)
        self.bt_rellas.setObjectName("bt_rellas")
        self.bt_gbg = QtWidgets.QToolButton(self.centralwidget)
        self.bt_gbg.setEnabled(True)
        self.bt_gbg.setGeometry(QtCore.QRect(80, 250, 221, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.bt_gbg.setFont(font)
        self.bt_gbg.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(13, 5, 81, 255), stop:1 rgba(36, 176, 189, 255));\n"
"color: rgb(255, 255, 255);\n"
"border-width:10px;\n"
"border-radius:20px;\n"
"")
        self.bt_gbg.setCheckable(False)
        self.bt_gbg.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.bt_gbg.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.bt_gbg.setAutoRaise(True)
        self.bt_gbg.setArrowType(QtCore.Qt.NoArrow)
        self.bt_gbg.setObjectName("bt_gbg")
        WelcomeUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(WelcomeUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 378, 21))
        self.menubar.setObjectName("menubar")
        WelcomeUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(WelcomeUI)
        self.statusbar.setObjectName("statusbar")
        WelcomeUI.setStatusBar(self.statusbar)

        self.retranslateUi(WelcomeUI)
        QtCore.QMetaObject.connectSlotsByName(WelcomeUI)

    def retranslateUi(self, WelcomeUI):
        _translate = QtCore.QCoreApplication.translate
        WelcomeUI.setWindowTitle(_translate("WelcomeUI", "atCrawl"))
        self.bt_skroutz.setText(_translate("WelcomeUI", "skroutz.gr"))
        self.bt_antallaktika.setText(_translate("WelcomeUI", "antallaktikaonline.gr"))
        self.bt_tripadvisor.setText(_translate("WelcomeUI", "tripadvisor.com"))
        self.header.setHtml(_translate("WelcomeUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Century Gothic\'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-style:italic; color:#dadada;\">atCrawl Services</span></p></body></html>"))
        self.bt_spitogatos.setText(_translate("WelcomeUI", "spitogatos.gr"))
        self.bt_booking.setText(_translate("WelcomeUI", "booking.com"))
        self.bt_rellas.setText(_translate("WelcomeUI", "rellasamortiser.gr"))
        self.bt_gbg.setText(_translate("WelcomeUI", "gbg-eshop.gr"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WelcomeUI = QtWidgets.QMainWindow()
    ui = Ui_WelcomeUI()
    ui.setupUi(WelcomeUI)
    WelcomeUI.show()
    sys.exit(app.exec_())

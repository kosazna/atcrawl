# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'atcrawl_crawler_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CrawlerUI(object):
    def setupUi(self, CrawlerUI):
        CrawlerUI.setObjectName("CrawlerUI")
        CrawlerUI.resize(780, 480)
        CrawlerUI.setStyleSheet("background-color: rgb(214, 214, 214);")
        self.centralwidget = QtWidgets.QWidget(CrawlerUI)
        self.centralwidget.setObjectName("centralwidget")
        self.label_url = QtWidgets.QLabel(self.centralwidget)
        self.label_url.setGeometry(QtCore.QRect(10, 60, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_url.setFont(font)
        self.label_url.setStyleSheet("")
        self.label_url.setObjectName("label_url")
        self.in_url = QtWidgets.QLineEdit(self.centralwidget)
        self.in_url.setGeometry(QtCore.QRect(70, 60, 701, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.in_url.setFont(font)
        self.in_url.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-width:4px;\n"
"border-color:black;\n"
"border-style:offset;\n"
"border-radius:10px;")
        self.in_url.setText("")
        self.in_url.setObjectName("in_url")
        self.bt_reset = QtWidgets.QToolButton(self.centralwidget)
        self.bt_reset.setGeometry(QtCore.QRect(670, 180, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.bt_reset.setFont(font)
        self.bt_reset.setStyleSheet("background-color: rgba(112, 112, 112, 0.8);\n"
"color: rgb(0, 0, 0);\n"
"border-width:10px;\n"
"border-radius:10px;\n"
"")
        self.bt_reset.setObjectName("bt_reset")
        self.label_brand = QtWidgets.QLabel(self.centralwidget)
        self.label_brand.setGeometry(QtCore.QRect(10, 180, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_brand.setFont(font)
        self.label_brand.setStyleSheet("")
        self.label_brand.setObjectName("label_brand")
        self.line_1 = QtWidgets.QFrame(self.centralwidget)
        self.line_1.setGeometry(QtCore.QRect(10, 160, 760, 16))
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.bt_launch = QtWidgets.QToolButton(self.centralwidget)
        self.bt_launch.setGeometry(QtCore.QRect(500, 110, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.bt_launch.setFont(font)
        self.bt_launch.setStyleSheet("background-color: rgba(112, 112, 112, 0.8);\n"
"color: rgb(0, 0, 0);\n"
"border-width:10px;\n"
"border-radius:10px;\n"
"")
        self.bt_launch.setObjectName("bt_launch")
        self.bt_collect = QtWidgets.QToolButton(self.centralwidget)
        self.bt_collect.setGeometry(QtCore.QRect(560, 180, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.bt_collect.setFont(font)
        self.bt_collect.setStyleSheet("background-color: rgba(112, 112, 112, 0.8);\n"
"color: rgb(0, 0, 0);\n"
"border-width:10px;\n"
"border-radius:10px;\n"
"")
        self.bt_collect.setObjectName("bt_collect")
        self.bt_export = QtWidgets.QToolButton(self.centralwidget)
        self.bt_export.setGeometry(QtCore.QRect(670, 410, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.bt_export.setFont(font)
        self.bt_export.setStyleSheet("background-color: rgba(112, 112, 112, 0.8);\n"
"color: rgb(0, 0, 0);\n"
"border-width:10px;\n"
"border-radius:10px;\n"
"")
        self.bt_export.setObjectName("bt_export")
        self.in_brand = QtWidgets.QLineEdit(self.centralwidget)
        self.in_brand.setGeometry(QtCore.QRect(90, 180, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.in_brand.setFont(font)
        self.in_brand.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-width:4px;\n"
"border-color:black;\n"
"border-style:offset;\n"
"border-radius:10px;")
        self.in_brand.setText("")
        self.in_brand.setObjectName("in_brand")
        self.label_discount = QtWidgets.QLabel(self.centralwidget)
        self.label_discount.setGeometry(QtCore.QRect(10, 230, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_discount.setFont(font)
        self.label_discount.setStyleSheet("")
        self.label_discount.setObjectName("label_discount")
        self.in_discount = QtWidgets.QLineEdit(self.centralwidget)
        self.in_discount.setGeometry(QtCore.QRect(90, 230, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.in_discount.setFont(font)
        self.in_discount.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-width:4px;\n"
"border-color:black;\n"
"border-style:offset;\n"
"border-radius:10px;")
        self.in_discount.setText("")
        self.in_discount.setObjectName("in_discount")
        self.label_pct = QtWidgets.QLabel(self.centralwidget)
        self.label_pct.setGeometry(QtCore.QRect(160, 230, 21, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_pct.setFont(font)
        self.label_pct.setStyleSheet("")
        self.label_pct.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pct.setObjectName("label_pct")
        self.in_folder = QtWidgets.QLineEdit(self.centralwidget)
        self.in_folder.setGeometry(QtCore.QRect(90, 410, 471, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.in_folder.setFont(font)
        self.in_folder.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-width:4px;\n"
"border-color:black;\n"
"border-style:offset;\n"
"border-radius:10px;")
        self.in_folder.setText("")
        self.in_folder.setObjectName("in_folder")
        self.label_folder = QtWidgets.QLabel(self.centralwidget)
        self.label_folder.setGeometry(QtCore.QRect(10, 410, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_folder.setFont(font)
        self.label_folder.setStyleSheet("")
        self.label_folder.setObjectName("label_folder")
        self.label_filename = QtWidgets.QLabel(self.centralwidget)
        self.label_filename.setGeometry(QtCore.QRect(10, 360, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_filename.setFont(font)
        self.label_filename.setStyleSheet("")
        self.label_filename.setObjectName("label_filename")
        self.in_filename = QtWidgets.QLineEdit(self.centralwidget)
        self.in_filename.setGeometry(QtCore.QRect(90, 360, 441, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.in_filename.setFont(font)
        self.in_filename.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-width:4px;\n"
"border-color:black;\n"
"border-style:offset;\n"
"border-radius:10px;")
        self.in_filename.setText("")
        self.in_filename.setObjectName("in_filename")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 340, 760, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_export = QtWidgets.QLabel(self.centralwidget)
        self.label_export.setGeometry(QtCore.QRect(10, 300, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_export.setFont(font)
        self.label_export.setStyleSheet("")
        self.label_export.setObjectName("label_export")
        self.bt_terminate = QtWidgets.QToolButton(self.centralwidget)
        self.bt_terminate.setGeometry(QtCore.QRect(670, 290, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.bt_terminate.setFont(font)
        self.bt_terminate.setStyleSheet("background-color: rgba(112, 112, 112, 0.8);\n"
"color: rgb(0, 0, 0);\n"
"border-width:10px;\n"
"border-radius:10px;\n"
"")
        self.bt_terminate.setObjectName("bt_terminate")
        self.bt_launch_collect = QtWidgets.QToolButton(self.centralwidget)
        self.bt_launch_collect.setGeometry(QtCore.QRect(610, 110, 160, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.bt_launch_collect.setFont(font)
        self.bt_launch_collect.setStyleSheet("background-color: rgba(112, 112, 112, 0.8);\n"
"color: rgb(0, 0, 0);\n"
"border-width:10px;\n"
"border-radius:10px;\n"
"")
        self.bt_launch_collect.setObjectName("bt_launch_collect")
        self.label_params = QtWidgets.QLabel(self.centralwidget)
        self.label_params.setGeometry(QtCore.QRect(10, 130, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_params.setFont(font)
        self.label_params.setStyleSheet("")
        self.label_params.setObjectName("label_params")
        self.label_domain = QtWidgets.QLabel(self.centralwidget)
        self.label_domain.setGeometry(QtCore.QRect(10, 10, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_domain.setFont(font)
        self.label_domain.setStyleSheet("")
        self.label_domain.setObjectName("label_domain")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(10, 40, 760, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.check_export = QtWidgets.QCheckBox(self.centralwidget)
        self.check_export.setGeometry(QtCore.QRect(650, 360, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.check_export.setFont(font)
        self.check_export.setChecked(True)
        self.check_export.setObjectName("check_export")
        self.status = QtWidgets.QLineEdit(self.centralwidget)
        self.status.setGeometry(QtCore.QRect(70, 100, 71, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.status.setFont(font)
        self.status.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.status.setStyleSheet("background-color: rgba(253, 4, 50, 0.8);\n"
"border-width:4px;\n"
"border-color:black;\n"
"color: rgb(0, 0, 0);\n"
"border-style:offset;\n"
"border-radius:10px;")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setObjectName("status")
        self.label_status = QtWidgets.QLabel(self.centralwidget)
        self.label_status.setGeometry(QtCore.QRect(10, 100, 51, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_status.setFont(font)
        self.label_status.setStyleSheet("")
        self.label_status.setObjectName("label_status")
        self.bt_reset_collect = QtWidgets.QToolButton(self.centralwidget)
        self.bt_reset_collect.setGeometry(QtCore.QRect(559, 220, 211, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.bt_reset_collect.setFont(font)
        self.bt_reset_collect.setStyleSheet("background-color: rgba(112, 112, 112, 0.8);\n"
"color: rgb(0, 0, 0);\n"
"border-width:10px;\n"
"border-radius:10px;\n"
"")
        self.bt_reset_collect.setObjectName("bt_reset_collect")
        self.browse_folder = QtWidgets.QToolButton(self.centralwidget)
        self.browse_folder.setGeometry(QtCore.QRect(570, 410, 31, 30))
        self.browse_folder.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-width:4px;\n"
"border-color:black;\n"
"border-style:offset;\n"
"border-radius:10px;")
        self.browse_folder.setObjectName("browse_folder")
        self.list_type = QtWidgets.QComboBox(self.centralwidget)
        self.list_type.setGeometry(QtCore.QRect(540, 360, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.list_type.setFont(font)
        self.list_type.setStyleSheet("background-color: rgba(112, 112, 112, 0.8);\n"
"color: rgb(0, 0, 0);\n"
"border-width:4px;\n"
"border-color:black;\n"
"border-radius:10px;")
        self.list_type.setObjectName("list_type")
        self.list_type.addItem("")
        self.list_type.addItem("")
        CrawlerUI.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(CrawlerUI)
        self.statusbar.setObjectName("statusbar")
        CrawlerUI.setStatusBar(self.statusbar)

        self.retranslateUi(CrawlerUI)
        QtCore.QMetaObject.connectSlotsByName(CrawlerUI)

    def retranslateUi(self, CrawlerUI):
        _translate = QtCore.QCoreApplication.translate
        CrawlerUI.setWindowTitle(_translate("CrawlerUI", "atCrawl"))
        self.label_url.setText(_translate("CrawlerUI", "URL"))
        self.bt_reset.setText(_translate("CrawlerUI", "reset"))
        self.label_brand.setText(_translate("CrawlerUI", "Brand"))
        self.bt_launch.setText(_translate("CrawlerUI", "launch"))
        self.bt_collect.setText(_translate("CrawlerUI", "collect"))
        self.bt_export.setText(_translate("CrawlerUI", "export"))
        self.label_discount.setText(_translate("CrawlerUI", "Discount"))
        self.label_pct.setText(_translate("CrawlerUI", "%"))
        self.label_folder.setText(_translate("CrawlerUI", "Folder"))
        self.label_filename.setText(_translate("CrawlerUI", "Filename"))
        self.label_export.setText(_translate("CrawlerUI", "Export"))
        self.bt_terminate.setText(_translate("CrawlerUI", "terminate"))
        self.bt_launch_collect.setText(_translate("CrawlerUI", "launch and collect"))
        self.label_params.setText(_translate("CrawlerUI", "Parameters"))
        self.label_domain.setText(_translate("CrawlerUI", "Domain"))
        self.check_export.setText(_translate("CrawlerUI", "export on finish"))
        self.status.setText(_translate("CrawlerUI", "offline"))
        self.label_status.setText(_translate("CrawlerUI", "Status"))
        self.bt_reset_collect.setText(_translate("CrawlerUI", "reset and collect"))
        self.browse_folder.setText(_translate("CrawlerUI", "..."))
        self.list_type.setItemText(0, _translate("CrawlerUI", "xlsx"))
        self.list_type.setItemText(1, _translate("CrawlerUI", "csv"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CrawlerUI = QtWidgets.QMainWindow()
    ui = Ui_CrawlerUI()
    ui.setupUi(CrawlerUI)
    CrawlerUI.show()
    sys.exit(app.exec_())

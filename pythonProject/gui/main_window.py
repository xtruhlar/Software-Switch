from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from .add_rule_window import Ui_Dialog
from .delete_rule_window import Ui_SelectRule
import sys
from PyQt5.QtGui import QIcon


def show_delete_popup(acl):  # Show a popup message
    Dialog = QtWidgets.QDialog()
    Dialog.setWindowFlags(Dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
    ui = Ui_SelectRule()
    ui.setupUi(Dialog)
    ui.update_table(acl)
    if Dialog.exec_() == QtWidgets.QDialog.Accepted:
        selected_rules = getattr(Dialog, 'x', None)
        if selected_rules:
            return selected_rules
    else:
        return None


def show_popup():  # Show a popup message
    Dialog = QtWidgets.QDialog()
    Dialog.setWindowFlags(Dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    if Dialog.exec_() == QtWidgets.QDialog.Accepted:
        created_rule = getattr(Dialog, 'rule', None)
        if created_rule:
            return created_rule

    else:
        return None


class Ui_MyMainWindow(object):
    def __init__(self):  # Initialize the main window
        self.sniffingLabel = None
        self.con = None
        self.statusITF1 = None
        self.statusITF2 = None
        self.stopButton = None
        self.startButton = None
        self.connectButton = None
        self.clientIPtext = None
        self.serverIPtext = None
        self.clientIP = None
        self.serverIP = None
        self.setTimer = None
        self.set_timer_field = None
        self.addButton = None
        self.Itf2OutLabel = None
        self.Itf2InLabel = None
        self.Itf1OutLabel = None
        self.Itf1InLabel = None
        self.clearButtonStats2 = None
        self.tableViewitf2out = None
        self.tableViewitf2in = None
        self.clearButtonStats1 = None
        self.tableViewitf1out = None
        self.tableViewitf1in = None
        self.itf1label = None
        self.itf2label = None
        self.itf1text = None
        self.itf2text = None
        self.menubar = None
        self.statusbar = None
        self.groupMenu = None
        self.delButton = None
        self.clearAllButton = None
        self.tableViewFilter = None
        self.groupFilters = None
        self.tableViewitf2 = None
        self.groupItf2 = None
        self.tableViewitf1 = None
        self.groupItf1 = None
        self.mac_table_table = None
        self.clearButton = None
        self.groupMAC = None
        self.centralwidget = None

    def setupUi(self, MyMainWindow):  # Set up the main window
        # --------------------------- Main Window --------------------------- #
        MyMainWindow.setObjectName("MyMainWindow")
        MyMainWindow.resize(1280, 950)
        MyMainWindow.setMaximumSize(QtCore.QSize(1280, 950))
        MyMainWindow.setMinimumSize(QtCore.QSize(1280, 950))

        # ------------------------------- Icon ------------------------------- #
        self.setWindowIcon(QIcon('src/icon_1.ico'))
        MyMainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MyMainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ------------------------------- GroupMAC --------------------------- #
        self.groupMAC = QtWidgets.QGroupBox(self.centralwidget)
        self.groupMAC.setGeometry(QtCore.QRect(340, 150, 600, 350))
        font = set_font(28)
        self.groupMAC.setFont(font)
        self.groupMAC.setAlignment(QtCore.Qt.AlignCenter)
        self.groupMAC.setObjectName("groupMAC")

        # --------------------- Group MAC - Clear Button --------------------- #
        self.clearButton = QtWidgets.QPushButton(self.groupMAC)
        self.clearButton.setGeometry(QtCore.QRect(25, 310, 100, 25))
        font = set_font(10)
        self.clearButton.setFont(font)
        self.clearButton.setObjectName("clearButton")

        # ----------------------- Group MAC - MAC Table ---------------------- #
        self.mac_table_table = QtWidgets.QTableView(self.groupMAC)
        self.mac_table_table.setGeometry(QtCore.QRect(30, 50, 540, 250))
        font = set_font(9)
        self.mac_table_table.setFont(font)
        self.mac_table_table.setObjectName("mac_table_table")
        self.mac_table_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # ------------------------- set_timer_field -------------------------- #
        self.set_timer_field = QtWidgets.QSpinBox(self.groupMAC)
        self.set_timer_field.setGeometry(QtCore.QRect(350, 305, 100, 35))
        font = set_font(8)
        self.set_timer_field.setValue(30)
        self.set_timer_field.setFont(font)
        self.set_timer_field.setObjectName("set_timer_field")

        # ----------------------------- setTimer ----------------------------- #
        self.setTimer = QtWidgets.QPushButton(self.groupMAC)
        self.setTimer.setGeometry(QtCore.QRect(470, 310, 100, 25))
        font = set_font(10)
        self.setTimer.setFont(font)
        self.setTimer.setObjectName("setTimer")

        # ----------------------------- groupItf1 ---------------------------- #
        # Group groupItf1 - Interface 1
        self.groupItf1 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupItf1.setGeometry(QtCore.QRect(25, 150, 250, 380))
        font = set_font(14)
        self.groupItf1.setFont(font)
        self.groupItf1.setAlignment(QtCore.Qt.AlignCenter)
        self.groupItf1.setObjectName("groupItf1")

        # ------------------------- tableViewitf1in -------------------------- #
        self.tableViewitf1in = \
            init_table_to_remove_duplicates(self.groupItf1, "tableViewitf1in",
                                            QtCore.QRect(5, 60, 115, 280))

        # ------------------------- tableViewitf1out ------------------------- #
        self.tableViewitf1out = \
            init_table_to_remove_duplicates(self.groupItf1, "tableViewitf1out",
                                            QtCore.QRect(130, 60, 115, 280))

        # ------------------------ clearButtonStats1 ------------------------- #
        self.clearButtonStats1 = QtWidgets.QPushButton(self.groupItf1)
        self.clearButtonStats1.setGeometry(QtCore.QRect(75, 350, 100, 25))
        font = set_font(10)
        self.clearButtonStats1.setFont(font)
        self.clearButtonStats1.setObjectName("clearButtonStats1")

        # --------------------------- Itf1InLabel ---------------------------- #
        self.Itf1InLabel = QtWidgets.QLabel(self.groupItf1)
        self.Itf1InLabel.setGeometry(QtCore.QRect(5, 40, 115, 20))
        font = set_font(12)
        self.Itf1InLabel.setFont(font)
        self.Itf1InLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Itf1InLabel.setObjectName("Itf1InLabel")

        # --------------------------- Itf1OutLabel --------------------------- #
        self.Itf1OutLabel = QtWidgets.QLabel(self.groupItf1)
        self.Itf1OutLabel.setGeometry(QtCore.QRect(130, 40, 115, 20))
        self.Itf1OutLabel.setFont(font)
        self.Itf1OutLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Itf1OutLabel.setObjectName("Itf1OutLabel")

        # ---------------------------- groupItf2 ----------------------------- #
        self.groupItf2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupItf2.setGeometry(QtCore.QRect(1005, 150, 250, 380))
        font = set_font(14)
        self.groupItf2.setFont(font)
        self.groupItf2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupItf2.setObjectName("groupItf2")

        # -------------------------- tableViewitf2in ------------------------- #
        self.tableViewitf2in = \
            init_table_to_remove_duplicates(self.groupItf2, "tableViewitf2in",
                                            QtCore.QRect(5, 60, 115, 280))

        # ------------------------- tableViewitf2out ------------------------- #
        self.tableViewitf2out = \
            init_table_to_remove_duplicates(self.groupItf2, "tableViewitf2out",
                                            QtCore.QRect(130, 60, 115, 280))

        # ------------------------- clearButtonStats2 ------------------------ #
        self.clearButtonStats2 = QtWidgets.QPushButton(self.groupItf2)
        self.clearButtonStats2.setGeometry(QtCore.QRect(75, 350, 100, 25))
        font = set_font(10)
        self.clearButtonStats2.setFont(font)
        self.clearButtonStats2.setObjectName("clearButtonStats2")

        # --------------------------- Itf2InLabel ---------------------------- #
        self.Itf2InLabel = QtWidgets.QLabel(self.groupItf2)
        self.Itf2InLabel.setGeometry(QtCore.QRect(5, 40, 115, 20))
        font = set_font(12)
        self.Itf2InLabel.setFont(font)
        self.Itf2InLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Itf2InLabel.setObjectName("Itf1InLabel_2")

        # --------------------------- Itf2OutLabel --------------------------- #
        self.Itf2OutLabel = QtWidgets.QLabel(self.groupItf2)
        self.Itf2OutLabel.setGeometry(QtCore.QRect(130, 40, 115, 20))
        self.Itf2OutLabel.setFont(font)
        self.Itf2OutLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Itf2OutLabel.setObjectName("Itf1OutLabel_2")

        # --------------------------- groupFilters --------------------------- #
        self.groupFilters = QtWidgets.QGroupBox(self.centralwidget)
        self.groupFilters.setGeometry(QtCore.QRect(25, 525, 1230, 325))
        font = set_font(14)
        self.groupFilters.setFont(font)
        self.groupFilters.setAlignment(QtCore.Qt.AlignCenter)
        self.groupFilters.setObjectName("groupFilters")

        # -------------------------- tableViewFilter ------------------------- #
        self.tableViewFilter = QtWidgets.QTableView(self.groupFilters)
        self.tableViewFilter.setGeometry(QtCore.QRect(50, 25, 1110, 250))
        font = set_font(8)
        self.tableViewFilter.setFont(font)
        self.tableViewFilter.setObjectName("tableViewFilter")
        # disable horizontal and vertical scroll bars
        self.tableViewFilter.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableViewFilter.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableViewFilter.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #e7e7e7; border: 0 px solid #e7e7e7; border-top: 0px; font-size: 10pt; font-family: OCR A Extended; }")

        # -------------------------- clearAllButton -------------------------- #
        self.clearAllButton = QtWidgets.QPushButton(self.groupFilters)
        self.clearAllButton.setGeometry(QtCore.QRect(1115, 285, 100, 25))
        font = set_font(10)
        self.clearAllButton.setFont(font)
        self.clearAllButton.setObjectName("clearAllButton")

        # ---------------------------- delButton ----------------------------- #
        self.delButton = QtWidgets.QPushButton(self.groupFilters)
        self.delButton.setGeometry(QtCore.QRect(1005, 285, 100, 25))
        self.delButton.setFont(font)
        self.delButton.setObjectName("delButton")

        # ----------------------------- addButton ---------------------------- #
        self.addButton = QtWidgets.QPushButton(self.groupFilters)
        self.addButton.setGeometry(QtCore.QRect(895, 285, 100, 25))
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")

        # ---------------------------- groupMenu ----------------------------- #
        self.groupMenu = QtWidgets.QGroupBox(self.centralwidget)
        self.groupMenu.setGeometry(QtCore.QRect(25, 5, 1230, 130))
        font = set_font(19)
        self.groupMenu.setFont(font)
        self.groupMenu.setAlignment(QtCore.Qt.AlignCenter)
        self.groupMenu.setObjectName("groupMenu")

        # -------------------------- serverIP -------------------------------- #
        self.serverIP = QtWidgets.QTextEdit(self.groupMenu)
        font = set_font(10)
        self.serverIP.setFont(font)
        self.serverIP.setGeometry(QtCore.QRect(360, 90, 200, 30))
        self.serverIP.setObjectName("serverIP")

        # -------------------------- clientIP -------------------------------- #
        self.clientIP = QtWidgets.QTextEdit(self.groupMenu)
        self.clientIP.setFont(font)
        self.clientIP.setGeometry(QtCore.QRect(580, 90, 200, 30))
        self.clientIP.setObjectName("clientIP")

        # -------------------------- serverIP -------------------------------- #
        self.con = QtWidgets.QLabel(self.groupMenu)
        self.con.setGeometry(QtCore.QRect(560, 90, 20, 30))
        font = set_font(10)
        self.con.setFont(font)
        self.con.setObjectName("con")

        # -------------------------- serverIPtext ----------------------------- #
        self.serverIPtext = QtWidgets.QLabel(self.groupMenu)
        self.serverIPtext.setGeometry(QtCore.QRect(360, 60, 200, 30))
        font = set_font(12)
        self.serverIPtext.setFont(font)
        self.serverIPtext.setToolTipDuration(-2)
        self.serverIPtext.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.serverIPtext.setAlignment(QtCore.Qt.AlignCenter)
        self.serverIPtext.setObjectName("serverIPtext")

        # -------------------------- clientIPtext ----------------------------- #
        self.clientIPtext = QtWidgets.QLabel(self.groupMenu)
        self.clientIPtext.setGeometry(QtCore.QRect(580, 60, 200, 30))
        self.clientIPtext.setFont(font)
        self.clientIPtext.setToolTipDuration(-2)
        self.clientIPtext.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.clientIPtext.setAlignment(QtCore.Qt.AlignCenter)
        self.clientIPtext.setObjectName("clientIPtext")

        # -------------------------- connectButton ---------------------------- #
        self.connectButton = QtWidgets.QPushButton(self.groupMenu)
        self.connectButton.setGeometry(QtCore.QRect(790, 90, 120, 30))
        font = set_font(10)
        self.connectButton.setFont(font)
        self.connectButton.setObjectName("connectButton")

        # ---------------------------- itf1label ----------------------------- #
        self.itf1label = QtWidgets.QLabel(self.groupMenu)
        self.itf1label.setGeometry(QtCore.QRect(20, 25, 200, 30))
        font = set_font(12)
        self.itf1label.setFont(font)
        self.itf1label.setObjectName("itf1label")

        # ---------------------------- itf2label ----------------------------- #
        self.itf2label = QtWidgets.QLabel(self.groupMenu)
        self.itf2label.setGeometry(QtCore.QRect(1010, 25, 200, 30))
        self.itf2label.setFont(font)
        self.itf2label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.itf2label.setObjectName("itf2label")

        # ----------------------------- itf1text ----------------------------- #
        self.itf1text = QtWidgets.QLabel(self.groupMenu)
        self.itf1text.setGeometry(QtCore.QRect(20, 60, 250, 30))
        self.itf1text.setObjectName("itf1text")

        # ----------------------------- itf2text ----------------------------- #
        self.itf2text = QtWidgets.QLabel(self.groupMenu)
        self.itf2text.setGeometry(QtCore.QRect(960, 60, 250, 30))
        self.itf2text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.itf2text.setObjectName("itf2text")

        # --------------------------- startButton ---------------------------- #
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(530, 860, 100, 35))
        font = set_font(10)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")

        # ---------------------------- stopButton ---------------------------- #
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(650, 860, 100, 35))
        self.stopButton.setFont(font)
        self.stopButton.setObjectName("stopButton")

        # ---------------------------- statusITF1 ---------------------------- #
        self.statusITF1 = QtWidgets.QLabel(self.groupMenu)
        self.statusITF1.setGeometry(QtCore.QRect(0, 25, 30, 30))
        font = set_font(9)
        self.statusITF1.setFont(font)
        self.statusITF1.setObjectName("statusITF1")

        # ---------------------------- statusITF2 ---------------------------- #
        self.statusITF2 = QtWidgets.QLabel(self.groupMenu)
        self.statusITF2.setGeometry(QtCore.QRect(1045, 25, 30, 30))
        self.statusITF2.setFont(font)
        self.statusITF2.setObjectName("statusITF2")

        # -------------------------- SniffingLable --------------------------- #
        self.sniffingLabel = QtWidgets.QLabel(self.centralwidget)
        self.sniffingLabel.setGeometry(QtCore.QRect(580, 900, 200, 20))
        self.sniffingLabel.setObjectName("sniffingLabel")
        font = set_font(10)
        self.sniffingLabel.setFont(font)

        MyMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MyMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 26))
        self.menubar.setObjectName("menubar")
        MyMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MyMainWindow)
        self.statusbar.setObjectName("statusbar")
        MyMainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MyMainWindow)
        QtCore.QMetaObject.connectSlotsByName(MyMainWindow)

    def retranslateUi(self, MyMainWindow):  # Set the text and titles
        _translate = QtCore.QCoreApplication.translate
        MyMainWindow.setWindowTitle(_translate("MyMainWindow", "Software Multilayer Switch"))
        self.groupMAC.setTitle(_translate("MyMainWindow", "MAC Table"))
        self.clearButton.setText(_translate("MyMainWindow", "Clear"))
        self.groupItf1.setTitle(_translate("MyMainWindow", "Interface 1"))
        self.clearButtonStats1.setText(_translate("MyMainWindow", "Clear"))
        self.setTimer.setText(_translate("MyMainWindow", "Set"))
        self.set_timer_field.setSuffix(_translate("MyMainWindow", "s"))
        self.Itf1InLabel.setText(_translate("MyMainWindow", "In"))
        self.Itf1OutLabel.setText(_translate("MyMainWindow", "Out"))
        self.groupItf2.setTitle(_translate("MyMainWindow", "Interface 2"))
        self.clearButtonStats2.setText(_translate("MyMainWindow", "Clear"))
        self.Itf2InLabel.setText(_translate("MyMainWindow", "In"))
        self.Itf2OutLabel.setText(_translate("MyMainWindow", "Out"))
        self.groupFilters.setTitle(_translate("MyMainWindow", "Filters"))
        self.clearAllButton.setText(_translate("MyMainWindow", "Clear All"))
        self.delButton.setText(_translate("MyMainWindow", "Delete"))
        self.addButton.setText(_translate("MyMainWindow", "Add"))
        self.groupMenu.setTitle(_translate("MyMainWindow", "PSIP L2 Software Multilayer Switch"))
        self.itf1label.setText(_translate("MyMainWindow", "Interface 1:"))
        self.itf2label.setText(_translate("MyMainWindow", "Interface 2:"))
        self.itf1text.setText(_translate("MyMainWindow", "TEXT"))
        self.itf2text.setText(_translate("MyMainWindow", "TEXT"))
        self.serverIPtext.setText(_translate("MyMainWindow", "Syslog Server IP"))
        self.clientIPtext.setText(_translate("MyMainWindow", "Syslog Client IP"))
        self.connectButton.setText(_translate("MyMainWindow", "Connect"))
        self.stopButton.setText(_translate("MyMainWindow", "Stop"))
        self.startButton.setText(_translate("MyMainWindow", "Start"))
        self.statusITF1.setText(_translate("MyMainWindow", "🔴"))
        self.statusITF2.setText(_translate("MyMainWindow", "🔴"))
        self.con.setText(_translate("MyMainWindow", "🔒"))
        self.sniffingLabel.setText(_translate("MyMainWindow", "Not Sniffing"))


def init_table_to_remove_duplicates(parent, name, geometry):  # Remove duplicate code
    table = QtWidgets.QTableView(parent)
    table.setGeometry(geometry)
    font = set_font(8)
    table.setFont(font)
    table.setObjectName(name)
    table.horizontalHeader().setVisible(False)
    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    return table


def set_font(size):  # Remove duplicate code
    font = QtGui.QFont()
    font.setFamily("OCR A Extended")
    font.setPointSize(size)
    return font

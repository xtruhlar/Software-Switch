from PyQt5 import QtCore, QtGui, QtWidgets
from switch.utilities import get_interfaces
from switch.ACL import ACL, ACLRule


class Ui_Dialog(object):
    def __init__(self):  # Initialize the dialog
        self.req = None
        self.radioOut = None
        self.radioIn = None
        self.radioGroupInOut = None
        self.radioDeny = None
        self.radioGroupPermitDeny = None
        self.radioPermit = None
        self.tableWidget = None
        self.AddRule = None

    def setupUi(self, Dialog):
        # --------------------------------------------- Set the Window ---------------------------------------------- #
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 500)
        self.AddRule = QtWidgets.QDialogButtonBox(Dialog)
        self.AddRule.setGeometry(QtCore.QRect(0, 455, 350, 40))
        self.AddRule.setOrientation(QtCore.Qt.Horizontal)
        self.AddRule.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.AddRule.setObjectName("AddRule")
        # --------------------------------------------- Set the Window ---------------------------------------------- #

        # ------------------------------------------- Set the window icon ------------------------------------------- #
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("src/acl_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setAutoFillBackground(True)
        # ------------------------------------------- Set the window icon ------------------------------------------- #

        # ------------------------------------------ Table for adding rules ----------------------------------------- #
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 350, 460))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(11)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        # ------------------------------------------ Table for adding rules ----------------------------------------- #

        # ---------------------------------------- Radio buttons Permit/Deny ---------------------------------------- #
        radioContainer = QtWidgets.QWidget()
        radioLayout = QtWidgets.QHBoxLayout(radioContainer)
        self.radioGroupPermitDeny = QtWidgets.QButtonGroup(Dialog)
        self.radioPermit = QtWidgets.QRadioButton("Permit")
        self.radioGroupPermitDeny.addButton(self.radioPermit)
        radioLayout.addWidget(self.radioPermit)
        self.radioDeny = QtWidgets.QRadioButton("Deny")
        self.radioGroupPermitDeny.addButton(self.radioDeny)
        radioLayout.addWidget(self.radioDeny)
        radioContainer.setLayout(radioLayout)
        self.tableWidget.setCellWidget(1, 0, radioContainer)
        # ---------------------------------------- Radio buttons Permit/Deny ---------------------------------------- #

        # ------------------------------------------ Radio buttons In / Out ----------------------------------------- #
        radioContainer = QtWidgets.QWidget()
        radioLayout = QtWidgets.QHBoxLayout(radioContainer)
        self.radioGroupInOut = QtWidgets.QButtonGroup(Dialog)
        self.radioIn = QtWidgets.QRadioButton("In")
        self.radioGroupInOut.addButton(self.radioIn)
        radioLayout.addWidget(self.radioIn)
        self.radioOut = QtWidgets.QRadioButton("Out")
        self.radioGroupInOut.addButton(self.radioOut)
        radioLayout.addWidget(self.radioOut)
        radioContainer.setLayout(radioLayout)
        self.tableWidget.setCellWidget(2, 0, radioContainer)
        # ------------------------------------------ Radio buttons In / Out ----------------------------------------- #

        # ----------------------------------------- Combo box for interfaces ---------------------------------------- #
        comboBox = QtWidgets.QComboBox()
        ports = get_interfaces()
        for port in ports:
            comboBox.addItem(port)

        # Add the combo box to the table cell
        self.tableWidget.setCellWidget(3, 0, comboBox)
        # ----------------------------------------- Combo box for interfaces ---------------------------------------- #

        # ----------------------------------------- Combo box for protocols ----------------------------------------- #
        comboBox = QtWidgets.QComboBox()
        protocols = ["any", "tcp", "udp", "icmp"]
        for protocol in protocols:
            comboBox.addItem(protocol)

        self.tableWidget.setCellWidget(8, 0, comboBox)
        # ----------------------------------------- Combo box for protocols ----------------------------------------- #

        # ----------------------------------------- Add the required label ------------------------------------------ #
        self.req = QtWidgets.QLabel(Dialog)
        self.req.setText("* required")
        self.req.setGeometry(QtCore.QRect(20, 465, 60, 20))
        # ----------------------------------------- Add the required label ------------------------------------------ #

        # ------------------------------------------ Set the table headers ------------------------------------------ #
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #ffffff; border: 1px solid #e7e7e7; border-top: 0px; border-left: 0px; border-right: 0px;}")
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # ------------------------------------------ Set the table headers ------------------------------------------ #

        self.retranslateUi(Dialog)

        # ------------------------------------------- Connect the buttons ------------------------------------------- #
        self.AddRule.accepted.connect(lambda: self.create_acl_rule(Dialog))
        self.AddRule.rejected.connect(Dialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        # ------------------------------------------- Connect the buttons ------------------------------------------- #

    # --------------------------------------------- Create the ACL rule --------------------------------------------- #
    def create_acl_rule(self, Dialog):
        # -------------------------------------- Get the values from the table -------------------------------------- #
        # --------------------------------------------- Required fields --------------------------------------------- #
        if self.radioPermit.isChecked():
            permit_deny = "allow"
        elif self.radioDeny.isChecked():
            permit_deny = "deny"
        else:
            permit_deny = None

        if self.radioIn.isChecked():
            direction = "in"
        elif self.radioOut.isChecked():
            direction = "out"
        else:
            direction = None

        interface = self.tableWidget.cellWidget(3, 0).currentText()

        msg = QtWidgets.QMessageBox()
        if permit_deny is None or direction is None or interface is None:
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Permit/Deny, Direction, and Interface are required fields")
            msg.exec_()
            return
        # --------------------------------------------- Required fields --------------------------------------------- #

        # --------------------------------------------- Optional fields --------------------------------------------- #
        # ---------------------------------- Check if MAC is in the correct format ---------------------------------- #
        if self.tableWidget.item(4, 0):
            if len(self.tableWidget.item(4, 0).text()) != 17 or self.tableWidget.item(4, 0).text()[2] != ":" or \
                    self.tableWidget.item(4, 0).text()[5] != ":" or self.tableWidget.item(4, 0).text()[8] != ":" or \
                    self.tableWidget.item(4, 0).text()[11] != ":" or self.tableWidget.item(4, 0).text()[14] != ":":
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Invalid MAC address")
                msg.exec_()
                return
            else:
                src_mac = self.tableWidget.item(4, 0).text()
                src_mac = src_mac.lower()
                if src_mac == "":
                    src_mac = "any"
        else:
            src_mac = "any"
        if self.tableWidget.item(5, 0):
            if len(self.tableWidget.item(5, 0).text()) != 17 or self.tableWidget.item(5, 0).text()[2] != ":" or \
                    self.tableWidget.item(5, 0).text()[5] != ":" or self.tableWidget.item(5, 0).text()[8] != ":" or \
                    self.tableWidget.item(5, 0).text()[11] != ":" or self.tableWidget.item(5, 0).text()[14] != ":":
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Invalid MAC address")
                msg.exec_()
                return
            else:
                dst_mac = self.tableWidget.item(5, 0).text()
                dst_mac = dst_mac.lower()
                if dst_mac == "":
                    dst_mac = "any"
        else:
            dst_mac = "any"
        # ---------------------------------- Check if MAC is in the correct format ---------------------------------- #

        # ---------------------------------- Check if IP is in the correct format ----------------------------------- #
        if self.tableWidget.item(6, 0):
            if len(self.tableWidget.item(6, 0).text().split(".")) != 4 or \
                    not all(0 <= int(num) <= 255 for num in self.tableWidget.item(6, 0).text().split(".")):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Invalid IP address")
                msg.exec_()
                return
            else:
                src_ip = self.tableWidget.item(6, 0).text()
                if src_ip == "":
                    src_ip = "any"
        else:
            src_ip = "any"
        if self.tableWidget.item(7, 0):
            if len(self.tableWidget.item(7, 0).text().split(".")) != 4 or \
                    not all(0 <= int(num) <= 255 for num in self.tableWidget.item(7, 0).text().split(".")):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Invalid IP address")
                msg.exec_()
                return
            else:
                dst_ip = self.tableWidget.item(7, 0).text()
                if dst_ip == "":
                    dst_ip = "any"
        else:
            dst_ip = "any"
        # ---------------------------------- Check if IP is in the correct format ----------------------------------- #

        # ---------------------------------------------- Get protocol ----------------------------------------------- #
        protocol = self.tableWidget.cellWidget(8, 0).currentText()
        # ---------------------------------------------- Get protocol ----------------------------------------------- #

        # ---------------------------------- Check if port is in the correct format ---------------------------------- #
        if self.tableWidget.item(9, 0):
            if not self.tableWidget.item(9, 0).text().isdigit() or int(self.tableWidget.item(9, 0).text()) < 0 or \
                    int(self.tableWidget.item(9, 0).text()) > 65535:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Invalid port number")
                msg.exec_()
                return
            else:
                dst_port = self.tableWidget.item(9, 0).text()
        else:
            dst_port = "any"
        if self.tableWidget.item(10, 0):
            if not self.tableWidget.item(10, 0).text().isdigit() or int(self.tableWidget.item(10, 0).text()) < 0 or \
                    int(self.tableWidget.item(10, 0).text()) > 65535:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Invalid port number")
                msg.exec_()
                return
            else:
                src_port = self.tableWidget.item(10, 0).text()
        else:
            src_port = "any"
        # ---------------------------------- Check if port is in the correct format ---------------------------------- #

        if self.tableWidget.item(0, 0):
            position = self.tableWidget.item(0, 0).text()
            position = int(position)
        else:
            position = None

        # ------------------------------------------- Create the ACL rule ------------------------------------------- #
        Dialog.rule = ACLRule(action=permit_deny, direction=direction, interface=interface, src_mac=src_mac,
                              dst_mac=dst_mac,
                              src_ip=src_ip, dst_ip=dst_ip, protocol=protocol, dst_port=dst_port, src_port=src_port,
                              position=position)

        Dialog.accept()
        # ------------------------------------------- Create the ACL rule ------------------------------------------- #

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Rule"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Dialog", "Permit/Deny*"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Dialog", "Direction*"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Dialog", "Interface*"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("Dialog", "Source MAC"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("Dialog", "Destination MAC"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("Dialog", "Source IP"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("Dialog", "Destination IP"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("Dialog", "Protocol"))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(_translate("Dialog", "Destination Port"))
        item = self.tableWidget.verticalHeaderItem(10)
        item.setText(_translate("Dialog", "Source Port"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "Position"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Select"))

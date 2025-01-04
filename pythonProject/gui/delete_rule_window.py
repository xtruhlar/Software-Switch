from PyQt5 import QtCore, QtGui, QtWidgets
from switch.ACL import ACL, ACLRule


class Ui_SelectRule(object):
    def __init__(self):  # Initialize the variables
        self.label = None
        self.tableWidget = None
        self.buttonBox = None

    def setupUi(self, SelectRule):
        SelectRule.setObjectName("SelectRule")
        SelectRule.resize(1200, 400)  # Set the size of the window
        self.buttonBox = QtWidgets.QDialogButtonBox(SelectRule)
        self.buttonBox.setGeometry(QtCore.QRect(10, 340, 1180, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        # ------------------------------------------- Set the window icon ------------------------------------------- #
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("src/acl_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SelectRule.setWindowIcon(icon)
        SelectRule.setAutoFillBackground(True)

        # ------------------------------------------- Set the window icon ------------------------------------------- #

        # ------------------------------------------ Set the Table Widget ------------------------------------------- #
        self.tableWidget = QtWidgets.QTableWidget(SelectRule)
        self.tableWidget.setGeometry(QtCore.QRect(10, 80, 1160, 250))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setRowCount(0)
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(8)
        self.tableWidget.horizontalHeader().setFont(font)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, item)

        self.tableWidget.setColumnWidth(0, 50)  # Select
        self.tableWidget.setColumnWidth(1, 75)  # Priority
        self.tableWidget.setColumnWidth(2, 65)  # P/D
        self.tableWidget.setColumnWidth(3, 50)  # I/O
        self.tableWidget.setColumnWidth(4, 100)  # Interface
        self.tableWidget.setColumnWidth(5, 150)  # Src MAC
        self.tableWidget.setColumnWidth(6, 150)  # Src IP
        self.tableWidget.setColumnWidth(7, 150)  # Dst MAC
        self.tableWidget.setColumnWidth(8, 150)  # Dst IP
        self.tableWidget.setColumnWidth(9, 65)  # Protocol
        self.tableWidget.setColumnWidth(10, 65)  # S Port
        self.tableWidget.setColumnWidth(11, 65)  # D Port
        # ------------------------------------------ Set the Table Widget ------------------------------------------- #

        # ------------------------------------------- Set the Label Widget ------------------------------------------ #
        self.label = QtWidgets.QLabel(SelectRule)
        self.label.setGeometry(QtCore.QRect(15, 10, 1180, 60))
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        # ------------------------------------------- Set the Label Widget ------------------------------------------ #

        self.retranslateUi(SelectRule)

        # ------------------------------------------- Connect the buttons ------------------------------------------- #
        self.buttonBox.accepted.connect(lambda: self.get_selected_rules(SelectRule))  # type: ignore
        self.buttonBox.rejected.connect(SelectRule.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SelectRule)
        # ------------------------------------------- Connect the buttons ------------------------------------------- #

    def retranslateUi(self, SelectRule):
        _translate = QtCore.QCoreApplication.translate
        SelectRule.setWindowTitle(_translate("SelectRule", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("SelectRule", ""))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("SelectRule", "Priority"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("SelectRule", "P/D"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("SelectRule", "I/O"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("SelectRule", "Interface"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("SelectRule", "Src MAC"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("SelectRule", "Src IP"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("SelectRule", "Dst MAC"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("SelectRule", "Dst IP"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("SelectRule", "P"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("SelectRule", "S Port"))
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText(_translate("SelectRule", "D Port"))
        self.label.setText(_translate("SelectRule", "Delete Rule"))

    # ---------------------------------------------- Update the table ----------------------------------------------- #
    def update_table(self, acl):
        for rule in acl.rules:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem())
            self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(rule.position)))
            self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(rule.action))
            self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(rule.direction))
            self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(rule.interface))
            self.tableWidget.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(rule.src_mac))
            self.tableWidget.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem(rule.src_ip))
            self.tableWidget.setItem(rowPosition, 7, QtWidgets.QTableWidgetItem(rule.dst_mac))
            self.tableWidget.setItem(rowPosition, 8, QtWidgets.QTableWidgetItem(rule.dst_ip))
            self.tableWidget.setItem(rowPosition, 9, QtWidgets.QTableWidgetItem(rule.protocol))
            self.tableWidget.setItem(rowPosition, 10, QtWidgets.QTableWidgetItem(rule.src_port))
            self.tableWidget.setItem(rowPosition, 11, QtWidgets.QTableWidgetItem(rule.dst_port)
                                     )
            self.tableWidget.item(rowPosition, 0).setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.item(rowPosition, 0).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.item(rowPosition, 1).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.item(rowPosition, 2).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.item(rowPosition, 3).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.item(rowPosition, 4).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.item(rowPosition, 5).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.item(rowPosition, 6).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.item(rowPosition, 7).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.item(rowPosition, 8).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.item(rowPosition, 9).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.item(rowPosition, 10).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.item(rowPosition, 11).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.item(rowPosition, 0).setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

            for i in range(12):  # Set the font
                self.tableWidget.item(rowPosition, i).setFont(QtGui.QFont("OCR A Extended", 8))

    # ---------------------------------------------- Update the table ----------------------------------------------- #

    # ---------------------------------------------- Get selected rules --------------------------------------------- #
    def get_selected_rules(self, SelectRule):
        selected_rules = []
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 0).checkState() == QtCore.Qt.Checked:
                selected_rules.append(i)

        SelectRule.x = selected_rules
        SelectRule.accept()
    # ---------------------------------------------- Get selected rules --------------------------------------------- #

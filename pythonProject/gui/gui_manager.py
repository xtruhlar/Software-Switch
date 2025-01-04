import time

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer

from switch.switch import Switch
from gui.main_window import Ui_MyMainWindow, show_popup, show_delete_popup
from switch.utilities import update_table_view, calculate_ttl, update_status_indicator, get_interfaces, get_max_position
from switch.syslog_client import SyslogClient
from switch.ACL import ACL
from scapy.all import sendp, ARP, sniff, Ether

sniftextflag1 = True
sniftextflag2 = False


class MyMainWindow(QtWidgets.QMainWindow, Ui_MyMainWindow):
    def __init__(self, parent=None):  # Initialize the main window
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.syslog_client = SyslogClient()
        self.acl = ACL(self.syslog_client)
        self.software_switch = Switch(self.acl, self.syslog_client)

        # ------------------------------ Buttons and signals within MAC Table and ACL ------------------------------- #
        self.clearButton.clicked.connect(self.clear_mac_table)  # Clear the MAC table
        self.software_switch.signal_emitter.mac_table_updated.connect(self.update_tables)

        self.mac_table_update_timer = QTimer(self)  # Update GUI MAC table every second
        self.mac_table_update_timer.timeout.connect(self.refresh_mac_table)
        self.mac_table_update_timer.timeout.connect(self.update_acl)
        self.mac_table_update_timer.start(100)
        self.setTimer.clicked.connect(self.set_ttl)  # Set the TTL value
        # ------------------------------ Buttons and signals within MAC Table and ACL ------------------------------- #

        # ---------------------------------- Buttons and signals within Statistics ---------------------------------- #
        self.software_switch.signal_emitter.statistics_cleared.connect(self.clear_statistics_display)
        self.software_switch.signal_emitter.statistics_updated.connect(self.update_statistics_display)
        self.clearButtonStats1.clicked.connect(self.clear_stats1)  # Clear statistics for interfaces
        self.clearButtonStats2.clicked.connect(self.clear_stats2)
        # ---------------------------------- Buttons and signals within Statistics ---------------------------------- #

        # ---------------------------------- Buttons and signals within Start/Stop ---------------------------------- #
        self.startButton.clicked.connect(self.software_switch.start_all_sniffing)  # Start sniffing
        self.stopButton.clicked.connect(self.software_switch.stop_all_sniffing)  # Stop sniffing
        # ---------------------------------- Buttons and signals within Start/Stop ---------------------------------- #

        # --------------------------------------- Interface status indicators --------------------------------------- #
        self.software_switch.signal_emitter.interface_status_updated.connect(self.update_interface_status)
        self.software_switch.signal_emitter.acl_updated.connect(self.update_acl)
        # --------------------------------------- Interface status indicators --------------------------------------- #

        # ------------------------------------------- Set interface names ------------------------------------------- #
        self.set_interface_names()
        # ------------------------------------------- Set interface names ------------------------------------------- #

        # --------------------------------------------- Set syslog info --------------------------------------------- #
        self.connectButton.clicked.connect(self.init_syslog_client)
        # --------------------------------------------- Set syslog info --------------------------------------------- #

        # ---------------------------------------------- Set ACL rule ----------------------------------------------- #
        self.addButton.clicked.connect(self.add_rule)
        self.delButton.clicked.connect(self.del_rule)
        self.clearAllButton.clicked.connect(self.clear_all_rules)
        # ---------------------------------------------- Set ACL rule ----------------------------------------------- #

    # -------------------------------------------------- Statistics -------------------------------------------------- #
    def set_interface_names(self):  # Set the interface names
        interfaces = get_interfaces()
        names = list(interfaces.keys())
        self.itf1text.setText(names[0])
        self.itf2text.setText(names[1])
        self.groupItf1.setTitle(names[0])
        self.groupItf2.setTitle(names[1])

    def update_interface_status(self, interface_name, is_up):  # Update the interface status indicators
        if interface_name == self.itf1text.text():
            update_status_indicator(self.statusITF1, is_up)
        elif interface_name == self.itf2text.text():
            update_status_indicator(self.statusITF2, is_up)

    def clear_statistics_display(self):  # Clear the statistics display
        self.tableViewitf1in.setModel(QtGui.QStandardItemModel())
        self.tableViewitf1out.setModel(QtGui.QStandardItemModel())

    def update_statistics_display(self, stats):  # Update the statistics display
        for interface, interface_stats in stats.items():
            if interface == self.itf1text.text():
                update_table_view(self.tableViewitf1in, interface_stats["IN"])  # Update the IN statistics
                update_table_view(self.tableViewitf1out, interface_stats["OUT"])  # Update the OUT statistics
            elif interface == self.itf2text.text():
                update_table_view(self.tableViewitf2in, interface_stats["IN"])
                update_table_view(self.tableViewitf2out, interface_stats["OUT"])

    def clear_stats1(self):  # Clear the statistics for interface 1
        self.software_switch.clear_statistics(interface_name=self.itf1text.text())

    def clear_stats2(self):  # Clear the statistics for interface 2
        self.software_switch.clear_statistics(interface_name=self.itf2text.text())

    # -------------------------------------------------- Statistics -------------------------------------------------- #

    # -------------------------------------------------- MAC Table -------------------------------------------------- #
    def refresh_mac_table(self):  # Refresh the MAC table
        if self.software_switch and self.software_switch.mac_table:
            self.update_tables(self.software_switch.mac_table.table)

    def clear_mac_table(self):  # Clear the MAC table
        self.software_switch.clear_mac_table()

    def update_tables(self, mac_table):  # Update the MAC table
        global sniftextflag1
        global sniftextflag2
        mac_table_model = QtGui.QStandardItemModel()  # Create a new model
        mac_table_model.setHorizontalHeaderLabels(["MAC Address", "Port", "Time to Live"])
        prev = self.software_switch.mac_table.prev_ttl
        actual = self.software_switch.mac_table.ttl
        for mac, (port, ts) in mac_table.items():  # Add the MAC table entries to the model
            if prev is not None and actual is not None:  # TTL calculation based on different scenarios
                if prev > actual:
                    ttl = calculate_ttl(ts, self.software_switch.mac_table.ttl, "0")
                    time_passed = time.time() - ts
                    self.software_switch.mac_table.table[mac] = (port, ts + time_passed)
                    self.software_switch.mac_table.prev_ttl = actual
                if prev < actual:
                    ttl = calculate_ttl(ts, self.software_switch.mac_table.ttl, prev)
                    self.software_switch.mac_table.table[mac] = (port, ts - int(ttl))
                if prev == actual:
                    ttl = calculate_ttl(ts, self.software_switch.mac_table.ttl, "2")
            else:
                ttl = calculate_ttl(ts, self.software_switch.mac_table.ttl, "2")
            row = [QtGui.QStandardItem(mac), QtGui.QStandardItem(port), QtGui.QStandardItem(ttl)]
            mac_table_model.appendRow(row)
        self.software_switch.mac_table.prev_ttl = None

        # Remove entry if TTL is 0
        for i in range(mac_table_model.rowCount()):
            if int(mac_table_model.item(i, 2).text()) <= 0:
                self.software_switch.mac_table.remove_entry(mac_table_model.item(i, 0).text())

        self.mac_table_table.setModel(mac_table_model)  # Set the model for the MAC table
        self.mac_table_table.resizeRowsToContents()
        if self.software_switch.ports[0].start_sniffing_flag is True \
                or self.software_switch.ports[1].start_sniffing_flag is True:
            if sniftextflag1 is True:  # Sniffing status
                self.sniffingLabel.setText("Sniffing.")
                sniftextflag1 = False
                sniftextflag2 = True
            elif sniftextflag2 is True:
                self.sniffingLabel.setText("Sniffing..")
                sniftextflag2 = False
            else:
                self.sniffingLabel.setText("Sniffing...")
                sniftextflag1 = True
        else:
            self.sniffingLabel.setText("Not Sniffing")

    def set_ttl(self):
        new_ttl = self.set_timer_field.value()  # Get the new TTL value
        self.software_switch.mac_table.set_ttl(new_ttl)  # Set the new TTL value
        self.syslog_client.send_log(f"Timer was changed to {new_ttl} seconds", "NOTICE-5", "MAC TABLE")

    # -------------------------------------------------- MAC Table -------------------------------------------------- #

    # ---------------------------------------------------- Syslog --------------------------------------------------- #
    def init_syslog_client(self):  # Initialize the SyslogClient
        if self.connectButton.text() == "Connect":
            server_ip, client_ip = self.get_ip_addresses()
            if server_ip and client_ip:
                self.syslog_client.start()
                self.syslog_client.setup(client_ip, server_ip)
                self.con.setText("🔓")  # Set the connection status indicator
                self.connectButton.setText("Disconnect")
        elif self.connectButton.text() == "Disconnect":
            self.con.setText("🔒")
            self.syslog_client.stop()
            self.connectButton.setText("Connect")

    def get_ip_addresses(self):  # Get the IP addresses from the text fields
        if not self.serverIP.toPlainText().strip() or not self.clientIP.toPlainText().strip():
            return None, None
        # Check the format of IP address
        elif len(self.serverIP.toPlainText().strip().split('.')) != 4 or len(
                self.clientIP.toPlainText().strip().split('.')) != 4 \
                or not all(i.isdigit() for i in self.serverIP.toPlainText().strip().split('.')) or not all(
            i.isdigit() for i in self.clientIP.toPlainText().strip().split('.')) \
                or not all(0 <= int(i) <= 255 for i in self.serverIP.toPlainText().strip().split('.')) \
                or not all(0 <= int(i) <= 255 for i in self.clientIP.toPlainText().strip().split('.')):
            return None, None
        else:
            server_ip = self.serverIP.toPlainText().strip()
            client_ip = self.clientIP.toPlainText().strip()
            return server_ip, client_ip

    # ---------------------------------------------------- Syslog --------------------------------------------------- #

    # -------------------------------------------------- ACL rules -------------------------------------------------- #
    def update_acl(self):
        acl_model = QtGui.QStandardItemModel()
        acl_model.setHorizontalHeaderLabels(
            ["P/D", "I/O", "Iterface", "Src MAC", "Src IP", "Dst MAC", "Dst IP", "P", "S Port", "D Port", "   "])

        for rule in self.acl.rules:
            row = [QtGui.QStandardItem(rule.action), QtGui.QStandardItem(rule.direction),
                   QtGui.QStandardItem(rule.interface),
                   QtGui.QStandardItem(rule.src_mac), QtGui.QStandardItem(rule.src_ip),
                   QtGui.QStandardItem(rule.dst_mac),
                   QtGui.QStandardItem(rule.dst_ip), QtGui.QStandardItem(rule.protocol),
                   QtGui.QStandardItem(rule.src_port),
                   QtGui.QStandardItem(rule.dst_port)]
            acl_model.appendRow(row)
        self.tableViewFilter.setModel(acl_model)
        self.tableViewFilter.resizeRowsToContents()

        self.tableViewFilter.setColumnWidth(0, 65)
        self.tableViewFilter.setColumnWidth(1, 50)
        self.tableViewFilter.setColumnWidth(2, 150)
        self.tableViewFilter.setColumnWidth(3, 150)
        self.tableViewFilter.setColumnWidth(4, 150)
        self.tableViewFilter.setColumnWidth(5, 150)
        self.tableViewFilter.setColumnWidth(6, 150)
        self.tableViewFilter.setColumnWidth(7, 75)
        self.tableViewFilter.setColumnWidth(8, 75)
        self.tableViewFilter.setColumnWidth(9, 75)
        self.tableViewFilter.setColumnWidth(10, 5)

    def add_rule(self):  # Dialong for adding
        rule = show_popup()
        if rule:
            if rule.position is None:
                rule.position = get_max_position(self.acl) + 1
            self.acl.add_rule(rule)
        else:
            pass

    def del_rule(self):  # Dialog for deleting
        selected_rules = show_delete_popup(self.acl)
        if selected_rules:
            rules_to_delete = []
            for rule in selected_rules:
                rules_to_delete.append(self.acl.rules[rule])

            if len(rules_to_delete) >= 1:  # Log if more than one rule is deleted at once
                self.syslog_client.send_log(f"More than one rule was deleted", "NOTICE-5", "ACL")

            for rule in rules_to_delete:
                self.acl.delete_rule(rule)
                self.update_acl()
        else:
            pass

    def clear_all_rules(self):  # Clear all
        with self.acl.lock:
            self.acl.rules.clear()
            self.update_acl()
            self.syslog_client.send_log("ACL was cleared", "INFO-6", "ACL")
    # -------------------------------------------------- ACL rules -------------------------------------------------- #

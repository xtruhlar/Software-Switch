import time
from scapy.all import Ether, sendp
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.http import HTTP
import psutil
from collections import deque
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from .port import Port
from gui.main_window import Ui_MyMainWindow
from gui.signal_emitter import SignalEmitter
from .mac_table import MACTable
from .utilities import get_interfaces
from .syslog_client import SyslogClient
from .ACL import ACL, ACLRule


class Switch:
    def __init__(self, acl, syslog_client):
        p = get_interfaces()  # Get the interfaces
        interface1 = list(p.keys())[0]
        mac_address_1 = p[interface1]
        interface2 = list(p.keys())[1]
        mac_address_2 = p[interface2]
        self.syslog_client = syslog_client  # Create a syslog client
        self.acl = acl  # Create an ACL
        self.mac_table = MACTable()  # Create a MAC table
        self.ports = [
            Port(interface1, mac_address_1, self.process_packet, self.syslog_client, self.acl, self.mac_table),
            Port(interface2, mac_address_2, self.process_packet, self.syslog_client, self.acl,
                 self.mac_table)]  # Create two ports
        self.syslog_client.set_using_ports(self.ports)
        self.signal_emitter = SignalEmitter()  # Create a signal emitter
        self.cable_Checker = QTimer()  # Create a timer to check the cable status every second
        self.cable_Checker.start(500)
        self.cable_Checker.timeout.connect(self.check_cable_status)
        self.cable_Checker.timeout.connect(self.emit_statistics)
        self.recent_packets = deque(maxlen=25)  # Store the recent packets

    def process_packet(self, packet, interface):  # Process the packet
        src_mac = packet.src  # Get the source MAC address
        dst_mac = packet.dst  # Get the destination MAC address

        in_port_obj = next((p for p in self.ports if p.interface_name == interface), None)

        if src_mac.startswith("00:e") or dst_mac.startswith("00:e") or src_mac.startswith("f8:e") or dst_mac.startswith(
                "f8:e"):
            return  # Ignore the packet if MAC of Cisco devices and reductions

        with self.mac_table.lock:  # Lock the MAC table to prevent race conditions
            packetID = packet.show(dump=True)  # Get the packet ID
            packetID = hash(packetID)  # Hash the packet ID
            packetID = (packetID, time.time())

            if packetID[0] in [i[0] for i in
                               self.recent_packets]:  # Check if the packet was received in the last 5 seconds
                if time.time() - [i[1] for i in self.recent_packets if i[0] == packetID[0]][0] > 5:
                    self.recent_packets.clear()
                return

            self.recent_packets.append(packetID)  # Add the packet to the recent packets
            self.mac_table.add_entry(src_mac, interface)
            self.mac_table.table[src_mac] = (interface, time.time())  # Restart ttl
            self.signal_emitter.mac_table_updated.emit(self.mac_table.table)

        with self.mac_table.lock:  # Lock the MAC table and check if the destination MAC is in the table
            if dst_mac in self.mac_table.table:
                out_port = next((p for p in self.ports if p.interface_name == self.mac_table.table[dst_mac][0]), None)
                self.forward_packet(packet, out_port, in_port_obj)  # Forward the packet
                return
            else:
                self.broadcast_packet(packet, in_port_obj)  # Broadcast the packet
                return

    def broadcast_packet(self, packet, in_port):  # Broadcast the packet
        for port in self.ports:
            if port != in_port:
                if self.acl.evaluate_packet(packet, "out", port.interface_name) == "allow":  # Check the ACL rule
                    sendp(packet, iface=port.interface_name, verbose=False)
                    port.update_stats(packet, "OUT")
                    self.signal_emitter.statistics_updated.emit({in_port.interface_name: in_port.stats,
                                                                 port.interface_name: port.stats})  # Emit the statistics

    def forward_packet(self, packet, out_port, in_port):  # Forward the packet
        if out_port and in_port != out_port:
            if self.acl.evaluate_packet(packet, "out", out_port.interface_name) == "allow":
                sendp(packet, iface=out_port.interface_name, verbose=False)
                out_port.update_stats(packet, "OUT")
                self.signal_emitter.statistics_updated.emit({in_port.interface_name: in_port.stats,
                                                             out_port.interface_name: out_port.stats})  # Emit the statistics

    def clear_mac_table(self):  # Clear the MAC table
        self.mac_table.clear()
        self.log_activity("MAC Table was cleared", "INFO-6", "MAC TABLE")

        self.signal_emitter.mac_table_updated.emit(self.mac_table.table)

    def check_cable_status(self):  # Check the cable status
        for port in self.ports:
            try:
                is_up = psutil.net_if_stats()[port.interface_name].isup
                port.check_cable_status()
                self.signal_emitter.interface_status_updated.emit(port.interface_name, is_up)
            except KeyError:  # Interface not found - unplugged reduction
                self.log_activity(f"Interface {port.interface_name} was damaged", "ALERT-1", "INTERFACE")
                self.stop_all_sniffing()
                self.cable_Checker.stop()
                self.clear_statistics(port.interface_name)

    def start_all_sniffing(self):
        self.log_activity("Switch started sniffing", "INFO-6", "SWITCH")
        for i, port in enumerate(self.ports):  # Start sniffing on all ports
            if not port.is_alive():
                current_stats = port.get_statistics()  # Get the current statistics
                p = get_interfaces()
                interface_name = list(p.keys())[i]
                mac_address = p[interface_name]

                new_port = Port(interface_name, mac_address, self.process_packet,
                                self.syslog_client, self.acl, self.mac_table)  # Create a new port
                new_port.stats = current_stats  # Set the current statistics
                new_port.start_sniffing()  # Start sniffing
                self.ports[i] = new_port  # Replace the old port with the new port

    def stop_all_sniffing(self):  # Stop sniffing on all ports
        for port in self.ports:
            port.stop_sniffing()  # Stop sniffing

        for port in self.ports:
            if port.is_alive():
                port.join()

    def clear_statistics(self, interface_name):  # Clear the statistics for an interface
        for port in self.ports:
            if port.interface_name == interface_name:
                port.reset_stats()
                self.signal_emitter.statistics_cleared.emit()

    def log_activity(self, message, severity, specification):  # Log activity
        self.syslog_client.send_log(message, severity, specification)

    def emit_statistics(self):  # Emit the statistics
        stats = {port.interface_name: port.stats for port in self.ports}
        self.signal_emitter.statistics_updated.emit(stats)

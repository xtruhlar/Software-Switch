import time
from scapy.all import Ether, IP, TCP, UDP, ICMP, ARP
from scapy.all import sniff
from threading import Thread, Event
import psutil
import threading


class Port(Thread):
    def __init__(self, interface_name, mac_address, process_packet, syslog_client, acl, mac_table):
        super().__init__()
        self.timer = None
        self.interface_name = interface_name
        self.mac_address = mac_address
        self.process_packet = process_packet
        self.acl = acl
        self.mac_table = mac_table
        self.stats = {
            "IN": {"ETH": 0, "ARP": 0, "IP": 0, "TCP": 0, "UDP": 0, "ICMP": 0, "HTTP": 0, "HTTPS": 0, "Total": 0},
            "OUT": {"ETH": 0, "ARP": 0, "IP": 0, "TCP": 0, "UDP": 0, "ICMP": 0, "HTTP": 0, "HTTPS": 0, "Total": 0}
        }

        self.shutdown_event = Event()  # Event to signal shutdown
        self.start_sniffing_flag = False  # Flag to start/stop sniffing

        self.cable_isup = psutil.net_if_stats()[self.interface_name].isup  # Check if the cable is up
        self.syslog_client = syslog_client

    def run(self):  # Start sniffing and filter only ICMP messages
        while not self.shutdown_event.is_set():
            if self.start_sniffing_flag:
                sniff(iface=self.interface_name, prn=self.packet_handler,  # Start sniffing, call packet_handler
                      stop_filter=lambda x: self.shutdown_event.is_set() or not self.start_sniffing_flag,
                      timeout=1)  # Sniff for 1 second

    def start_sniffing(self):  # Start sniffing
        self.start_sniffing_flag = True
        self.start()

    def stop_sniffing(self):  # Stop sniffing
        self.start_sniffing_flag = False
        self.shutdown_event.set()
        self.syslog_client.send_log("Switch stopped sniffing", "INFO-6", "SWITCH")

    def packet_handler(self, packet):  # Process packet
        if not self.shutdown_event.is_set():
            if self.acl.evaluate_packet(packet, "in", self.interface_name) == "allow":  # Check ACL rule
                self.update_stats(packet, "IN")
                self.process_packet(packet, self.interface_name)
            else:
                pass

    def get_statistics(self):  # Get statistics
        return self.stats

    def reset_stats(self):  # Reset statistics
        self.stats = {
            "IN": {"ETH": 0, "ARP": 0, "IP": 0, "TCP": 0, "UDP": 0, "ICMP": 0, "HTTP": 0, "HTTPS": 0, "Total": 0},
            "OUT": {"ETH": 0, "ARP": 0, "IP": 0, "TCP": 0, "UDP": 0, "ICMP": 0, "HTTP": 0, "HTTPS": 0, "Total": 0}
        }
        self.syslog_client.send_log(f"Statistics cleated on interface: {self.interface_name}", "INFO-6", "INTERFACE")

    def update_stats(self, packet, direction):  # Update statistics
        if direction not in ["IN", "OUT"]:
            raise ValueError(f"Invalid direction: {direction}")
        else:
            self.stats[direction]["Total"] += 1
            if Ether in packet:
                self.stats[direction]["ETH"] += 1
                if IP in packet:
                    self.stats[direction]["IP"] += 1
                    if TCP in packet:
                        self.stats[direction]["TCP"] += 1
                        if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                            self.stats[direction]["HTTP"] += 1
                        elif packet[TCP].dport == 443 or packet[TCP].sport == 443:
                            self.stats[direction]["HTTPS"] += 1
                    elif UDP in packet:
                        self.stats[direction]["UDP"] += 1
                    elif ICMP in packet:
                        self.stats[direction]["ICMP"] += 1
                elif ARP in packet:
                    self.stats[direction]["ARP"] += 1

    def check_cable_status(self):
        current_status = psutil.net_if_stats()[self.interface_name].isup
        if not current_status and self.cable_isup:  # Cable was disconnected
            self.cable_isup = False
            self.timer = threading.Timer(5.0, self.remove_mac_entries)
            self.timer.start()
        elif current_status and not self.cable_isup:  # Cable was reconnected
            self.cable_isup = True
            if self.timer:
                self.timer.cancel()

    def remove_mac_entries(self):
        if not self.cable_isup:
            # Create a list of MAC addresses to remove
            macs_to_remove = [mac_address for mac_address, entry in self.mac_table.table.items() if
                              entry[0] == self.interface_name]

            self.syslog_client.send_log(f"Cable was unplugged from interface: {self.interface_name}", "INFO-6", "INTERFACE")
            # Remove the entries outside the iteration
            for mac_address in macs_to_remove:
                self.mac_table.remove_entry(mac_address)

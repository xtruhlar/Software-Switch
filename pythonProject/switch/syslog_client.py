import socket
import datetime
from scapy.all import IP, UDP, send, Ether, ARP, srp


class SyslogClient:
    def __init__(self):
        self.ports = None
        self.source_ip = None
        self.syslog_server_ip = None
        self.socket = None  # Socket to send syslog messages
        self.enabled = False  # Flag to enable/disable the client

    def close_socket(self):
        self.socket.close()  # Close the socket to stop sending syslog messages

    def set_using_ports(self, ports):
        self.ports = ports

    def setup(self, source_ip, syslog_server_ip):  # Set up the syslog client
        self.source_ip = source_ip
        self.syslog_server_ip = syslog_server_ip
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
        self.send_log("Syslog Client Initialized", "INFO-6", "SYSLOG")

    def send_log(self, message, severity, specification):  # Send a log message
        if not self.enabled:
            return
        timestamp = datetime.datetime.now().isoformat()
        syslog_message = f"{timestamp}: {severity}-{specification}: {message}"
        packet = IP(src=self.source_ip, dst=self.syslog_server_ip) / UDP(dport=514, sport=35000) / syslog_message
        for port in self.ports:
            send(packet, verbose=False, iface=port.interface_name)

    def start(self):
        self.enabled = True  # Enable the client

    def stop(self):
        self.send_log("Syslog Client Stopping...", "INFO-6", "SYSLOG")
        self.enabled = False  # Disable the client
        self.syslog_server_ip = None
        self.source_ip = None
        self.close_socket()  # Close the socket

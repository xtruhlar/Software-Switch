from threading import Lock
import scapy.all as scapy
from scapy.all import IP, TCP, UDP, ICMP, ARP


class ACLRule:
    def __init__(self, src_ip=None, dst_ip=None, src_mac=None, dst_mac=None, src_port=None, dst_port=None,
                 protocol=None, action=None, direction=None, interface=None, position=None):  # Create a rule
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.src_port = src_port
        self.dst_port = dst_port
        self.protocol = protocol
        self.action = action
        self.direction = direction
        self.interface = interface
        self.position = position


# ---------------------------------------------------- Match Rule --------------------------------------------------- #
def match_rule(packet, rule, in_out, interface, action):
    match = True

    if rule.interface is not None and rule.interface != interface:
        match = False
    if rule.direction is not None and rule.direction != in_out:
        match = False

    if ARP in packet:
        if action == "allow":
            match = True
        if action == "deny":
            match = False

    if IP in packet:
        if rule.src_ip is not None and rule.src_ip != "any" and packet[IP].src != rule.src_ip:
            match = False
        if rule.dst_ip is not None and rule.dst_ip != "any" and packet[IP].dst != rule.dst_ip:
            match = False

    if packet is not None:
        if rule.src_mac is not None and rule.src_mac != "any" and packet.src != rule.src_mac:
            match = False
        if rule.dst_mac is not None and rule.dst_mac != "any" and packet.dst != rule.dst_mac:
            match = False

    if TCP in packet:
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif UDP in packet:
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
    else:
        src_port = dst_port = None

    if rule.src_port is not None and rule.src_port != "any" and src_port != rule.src_port:
        match = False
    if rule.dst_port is not None and rule.dst_port != "any" and dst_port != rule.dst_port:
        match = False

    if rule.protocol is not None and rule.protocol != "any":
        if TCP in packet:
            protocol = 'tcp'
        elif UDP in packet:
            protocol = 'udp'
        elif ICMP in packet:
            protocol = 'icmp'
        else:
            protocol = None

        if protocol != rule.protocol:
            match = False

    return match


# ---------------------------------------------------- Match Rule --------------------------------------------------- #


class ACL:  # Access Control List
    def __init__(self, syslog_client):
        self.rules = []
        self.lock = Lock()  # Lock for thread safety
        self.syslog_client = syslog_client

    def add_rule(self, rule):  # Add a rule
        with self.lock:
            self.rules.append(rule)
            self.syslog_client.send_log(f"New rule in ACL", "INFO-6", "ACL")
            self.sort_rules_by_position()  # Sort the rules by position

    def delete_rule(self, rule):  # Delete a rule
        with self.lock:
            self.syslog_client.send_log(f"Rule removed from ACL", "INFO-6", "ACL")
            self.rules.remove(rule)

    def evaluate_packet(self, packet, in_out, interface):  # Evaluate the packet
        with self.lock:
            for rule in self.rules:
                if match_rule(packet, rule, in_out, interface, rule.action):
                    return rule.action
            return "allow"  # Default action if no rules match

    def sort_rules_by_position(self):
        self.rules.sort(key=lambda x: x.position)  # Sort the rules by position

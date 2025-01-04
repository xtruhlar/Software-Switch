import time
from threading import Lock


class MACTable:
    def __init__(self):
        self.ttl = 30  # Default time to live
        self.prev_ttl = 30  # Previous time to live, used in calculations
        self.table = {}
        self.lock = Lock()

    def set_ttl(self, new_ttl):  # Set time to live
        with self.lock:
            self.prev_ttl = self.ttl
            self.ttl = new_ttl

    def add_entry(self, mac_address, port_name):  # Add entry to the table
        self.table[mac_address] = (port_name, time.time())

    def remove_entry(self, mac_address):  # Remove entry
        with self.lock:
            if mac_address in self.table:
                del self.table[mac_address]

    def clear(self):  # Clear the table
        with self.lock:
            self.table.clear()

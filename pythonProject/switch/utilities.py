import psutil
from PyQt5 import QtGui
import time
import platform


def get_interfaces():  # Get the interfaces
    actual_system = platform.system()
    if actual_system == 'Windows':
        ports = get_interfaces_windows()
        return ports
    elif actual_system == 'Darwin':
        ports = get_interfaces_mac()
        return ports
    else:
        return 'Unsupported OS'

def get_interfaces_mac():
    ports = {}
    for intf, mac_addr in psutil.net_if_addrs().items():  # psutil for system information
        for i in mac_addr:
            if i.family == psutil.AF_LINK:  # if the family is a link - Ethernet
                ports[intf] = i.address  # add the interface and the mac address to the dictionary

    if 'lo0' not in ports or len(ports) < 2:
        ports['lo0'] = '00:00:00:00:00:00'  # Loopback interfaces do not have a MAC address

    return ports

def get_interfaces_windows():
    ports = {}
    for intf, mac_addr in psutil.net_if_addrs().items():  # psutil for system information
        for i in mac_addr:
            if i.family == psutil.AF_LINK:  # if the family is a link - Ethernet
                ports[intf] = i.address  # add the interface and the mac address to the dictionary

    keys_to_remove = [x for x in ports if "Ethernet" not in x or "vEthernet" in x or "en0" in x or "en1" in x]

    if 'Wi-Fi' in keys_to_remove:
        keys_to_remove.remove('Wi-Fi')
        keys_to_remove.remove('vEthernet (WSL (Hyper-V firewall))')

    for key in keys_to_remove:  # remove the keys that are not Ethernet
        del ports[key]

    return ports


def update_table_view(table_view, stats):  # Update the table view
    model = QtGui.QStandardItemModel()
    for protocol, count in stats.items():  # Add the statistics to the model
        row = [QtGui.QStandardItem(protocol), QtGui.QStandardItem(str(count))]
        model.appendRow(row)
    table_view.setModel(model)


def calculate_ttl(ts, get_ttl, op):  # Calculate the time to live
    # if new time is lower than the previous time, timestamp should start from the beginning
    if op == "0":
        ttl = get_ttl - (time.time() - ts)
        ttl += get_ttl - ttl
    elif op == "2":
        ttl = get_ttl - (time.time() - ts)
    else:
        ttl = get_ttl - (time.time() - ts)
        ttl = ttl - op

    if ttl < 0:
        ttl = 0
    ttl = "{:.0f}".format(ttl)
    return ttl


def update_status_indicator(label, is_up):  # Update the status indicator
    label.setText("🟢" if is_up else "🔴")  # Set the label text to green or red


def get_max_position(acl):
    if acl.rules:
        return max([rule.position for rule in acl.rules])
    return 0

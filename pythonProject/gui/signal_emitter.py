import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, QTimer


class SignalEmitter(QObject):
    mac_table_updated = pyqtSignal(object)  # Signal emitted when the MAC table is updated
    acl_updated = pyqtSignal(object)  # Signal emitted when the ACL is updated
    statistics_cleared = pyqtSignal()  # Signal emitted when the statistics are cleared
    statistics_updated = pyqtSignal(dict)  # Signal emitted when the statistics are updated
    ports_stopped = pyqtSignal()  # Signal emitted when all ports are stopped
    interface_status_updated = pyqtSignal(str, bool)  # Signal emitted when an interface status is updated
    syslog_info = pyqtSignal(str, str)  # Signal emitted when the syslog info is updated
    syslog_status_updated = pyqtSignal(str)  # Signal emitted when the syslog status is updated

# Multilayer Software Switch

This project implements a **Multilayer Software Switch** as a part of the Switching and Routing in IP Networks course (SS 2023/2024). The software is designed to meet specified requirements, including MAC table management, traffic statistics, and advanced features such as Access Control Lists and RESTCONF integration.

## Features

### 1. Media Access Control (MAC) Table
- The software switch dynamically learns and displays the MAC table.
- Records include the MAC address, associated port, and the remaining lifetime.
- Includes features to:
  - Automatically update MAC table entries.
  - Clear the MAC table via a GUI button.
  - Configure timers for MAC record expiration.
  - Handle cable disconnection and reconnection events effectively.

### 2. Traffic Statistics
- Displays real-time statistics for OSI layers 2-4 for each port, including:
  - Received and sent counters for Ethernet II, ARP, IP, TCP, UDP, ICMP, and HTTP traffic.
- Includes a reset button to clear statistics.

### 3. Access Control Lists (ACLs)
- Implements packet filtering without relying on built-in PCAP functions.
- Supports filtering by:
  - Source and destination MAC and IP addresses.
  - Transport layer ports and ICMP types.
- Allows combinations of rules, such as:
  - Enabling HTTP for a specific IP while disabling ICMP (ping) for a specific MAC.
- Displays the list of rules in the GUI, with options to delete them individually.
- Differentiates rules for incoming and outgoing traffic on each port.

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:xtruhlar/Software-Switch.git
   ```

## Usage

1. You have to run the `main.py` as sudo user (on macOS) so the software can use `scapy` lib.

2. Configure features:
    - Set MAC table timers.
    - Add, modify, or delete Access Control List rules.
    - Connect to Syslog server

3. Monitor and interact with the switch:
    - View MAC table and traffic statistics in real-time.
    - Use the GUI buttons to reset statistics or clear the MAC table.


_Note_: This project is a semestral assignment for educational purposes and may require adaptation for production use.
Let me know if you’d like further refinements!
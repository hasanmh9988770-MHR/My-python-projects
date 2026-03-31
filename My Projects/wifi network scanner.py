import os
import sys
from scapy.all import ARP, Ether, srp


def deep_scan(ip_range, interface):
    # SELF-CHECK: Are we running as Root/Sudo?
    if os.geteuid() != 0:
        print("\n[!] ERROR: Permission Denied.")
        print(f"Please run this in your terminal using:\nsudo {sys.executable} \"{sys.argv[0]}\"\n")
        sys.exit(1)

    print(f"Starting Deep Scan on {ip_range} via {interface}...")
    print("Nudging devices... please wait 7 seconds.")

    try:
        # 1. Prepare the ARP packet
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        # 2. Send the packet out of 'en1' (Wi-Fi)
        # timeout=7 gives slow phones/tablets time to wake up
        result = srp(packet, timeout=7, verbose=0, iface=interface)[0]

        devices = []
        for sent, received in result:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})

        return devices

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


if __name__ == "__main__":
    # Settings for your Mac Mini
    TARGET_IP_RANGE = "192.168.0.0/24"
    WIFI_INTERFACE = "en1"

    found_list = deep_scan(TARGET_IP_RANGE, WIFI_INTERFACE)

    print("\n" + "=" * 50)
    print(f"{'IP Address':<20} | {'MAC Address':<20} | {'Device'}")
    print("=" * 50)

    for device in found_list:
        vendor = "Unknown"
        # Label your known devices
        if device['ip'] == "192.168.0.1":
            vendor = "TP-Link Router"
        elif "b8:94:e7" in device['mac'].lower():
            vendor = "Samsung Device"

        print(f"{device['ip']:<20} | {device['mac']:<20} | {vendor}")

    print("=" * 50)
    print(f"Scan complete. Found {len(found_list)} active device(s).")
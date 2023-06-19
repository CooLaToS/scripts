#!/usr/bin/env python3

import subprocess

# Path to the .ovpn file
ovpn_file = '/etc/openvpn/openvpn.ovpn'

# Function to start the OpenVPN connection
def start_vpn():
    try:
        # Start the OpenVPN connection using subprocess
        subprocess.run(['sudo', 'openvpn', '--config', ovpn_file], check=True)
        print('VPN connection started successfully.')
    except subprocess.CalledProcessError as e:
        print(f'Error: Failed to start VPN connection.\n{e}')

# Main script logic
if __name__ == '__main__':
    # Start the VPN connection
    start_vpn()
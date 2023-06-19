import os
import shutil
import sys

# Check if the script is running with sudo
if os.geteuid() != 0:
    print("This script must be run with sudo. Please try again with sudo privileges.")
    sys.exit(1)

def create_service_unit():
    # Get service name
    service_name = "autoconnect-vpn"

    # Get .ovpn file path from user input
    while True:
        ovpn_file = input("Enter the path or filename of the .ovpn file: ")

        # Check if the .ovpn file exists in the specified path or next to the script
        if not os.path.isfile(ovpn_file):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            ovpn_file = os.path.join(script_dir, ovpn_file)

            if not os.path.isfile(ovpn_file):
                print(f"The .ovpn file '{ovpn_file}' does not exist. Please enter a valid file path or filename.")
                continue

        # Ensure the .ovpn file has the .ovpn extension
        if not ovpn_file.lower().endswith('.ovpn'):
            ovpn_file += '.ovpn'

        break

    # Move the .ovpn file to /etc/openvpn/openvpn.ovpn using sudo
    destination_file = '/etc/openvpn/openvpn.ovpn'
    shutil.move(ovpn_file, destination_file)
    print(f'.ovpn file moved to: {destination_file}')

    unit_content = f'''\
[Unit]
Description=Autoconnect VPN
After=network.target

[Service]
ExecStart=/usr/bin/python3 {os.path.abspath(os.path.dirname(__file__))}/autoconnect_VPN.py {destination_file}

[Install]
WantedBy=multi-user.target
'''

    unit_file = f'/etc/systemd/system/{service_name}.service'

    with open(unit_file, 'w') as file:
        file.write(unit_content)

    print(f'Service unit file created: {unit_file}')

    # Enable the service using sudo systemctl
    os.system(f"sudo systemctl enable {service_name}.service")
    print(f'Service {service_name}.service enabled.')

    # Ask the user if they want to restart and test the VPN connection
    restart = input("Do you want to start and test the VPN connection? (y/n): ")
    if restart.lower() == 'y':
        os.system("sudo systemctl start autoconnect-vpn.service")
        print("VPN connection started.")
    else:
        print("VPN connection not started.")

if __name__ == '__main__':
    create_service_unit()

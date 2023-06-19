# Autoconnect VPN Service

This repository contains scripts to create a systemd service that automatically connects to a VPN using OpenVPN.

## Prerequisites

- OpenVPN installed on the system
- Python 3

## Installation

1. Clone this repository:

   ```bash
   git clone -b VPN --single-branch https://github.com/CooLaToS/scripts.git
   ```

2. Change to the repository directory:
   
   ```bash
   cd scripts
   ```

3. Run the following command to create the systemd service: ( Please note that You will be prompted to provide the path or filename of the .ovpn file. Make sure to provide the correct file for your VPN configuration.)

    ```bash 
    sudo python3 create_service_unit.py
    ```

## Configuration

The `.ovpn` file contains the configuration details for your VPN connection. Make sure to provide the correct file path or filename when prompted.

## Troubleshooting

- If the `.ovpn` file is not found or specified incorrectly, you will be prompted to re-enter the path or filename.
- If the VPN connection fails to start, check the OpenVPN logs for more information.

## License

This project is licensed under the MIT License.

    

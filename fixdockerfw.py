#!/usr/bin/env python3

import os
import subprocess
import json
import docker 

def is_root():
    return os.geteuid() == 0

def check_docker_sdk():
    try:
        import docker
        print("Docker SDK for Python is already installed.")
    except ImportError:
        print("Docker SDK for Python is not found. Installing...")
        try:
            subprocess.run(['pip3', 'install', 'docker'], check=True)
            print("Docker SDK for Python has been installed.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during Docker SDK installation: {e}")
            sys.exit(1)
    
def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)

def update_docker_config():
    # Check if the file exists
    if not os.path.exists("/etc/docker/daemon.json"):
        with open("/etc/docker/daemon.json", "w") as file:
            # Writing a default empty JSON object
            file.write("{}")

    # Read the original data
    with open("/etc/docker/daemon.json", "r") as file:
        data = json.load(file)
    
    # Backup the original data
    with open("/etc/docker/daemon.json.bak", "w") as backup_file:
        json.dump(data, backup_file, indent=2)

    # Modify the data
    data["iptables"] = False

    # Write the modified data back to the original file
    with open("/etc/docker/daemon.json", "w") as file:
        json.dump(data, file, indent=2)

def restart_docker():
    run_command(["systemctl", "restart", "docker"])

def enable_ip_forwarding():
    run_command(['sh', '-c', 'echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf'])
    run_command(["sysctl", "-p"])

def update_ufw_config():
    run_command(['sed', '-i', 's/DEFAULT_FORWARD_POLICY="DROP"/DEFAULT_FORWARD_POLICY="ACCEPT"/', '/etc/default/ufw'])
    run_command(["ufw", "allow", "from", "172.20.0.0/16"])
    run_command(["ufw", "reload"])

def setup_nat():
    run_command(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-s', '172.20.0.0/16', '!', '-o', 'docker0', '-j', 'MASQUERADE'])
    run_command(["apt", "install", "-y", "iptables-persistent"])
    run_command(["netfilter-persistent", "save"])

def create_docker_network():
    # Create a Docker client instance
    client = docker.from_env()

    # Network configurations
    network_name = "CELLOCKNET"
    network_config = {
        "driver": "bridge",
        "ipam": docker.types.IPAMConfig(
            pool_configs=[
                docker.types.IPAMPool(
                    subnet='172.20.0.0/16',
                    gateway='172.20.0.1'
                )
            ]
        ),
        "enable_ipv6": False,
        "options": {}
    }

    # Check if the network already exists
    existing_networks = client.networks.list(names=[network_name])
    if existing_networks:
        print(f"Network '{network_name}' already exists!")
        return

    # Create the Docker network
    network = client.networks.create(name=network_name, **network_config)
    print(f"Network '{network_name}' created with ID {network.id}")

def main():
    if not is_root():
        print("Please run the script as root or with sudo.")
        return
    #Check if docker is install via pip install docker
    check_docker_sdk()
    
    # Handle Docker's Configuration
    update_docker_config()
    print("/etc/docker/daemon.json has been updated.")
    restart_docker()
    print("Docker daemon has been restarted.")

    # Create the Docker Network
    create_docker_network()   # <--- New function call

    # Handle IP Forwarding, UFW, and NAT setup
    enable_ip_forwarding()
    print("IP Forwarding enabled.")
    update_ufw_config()
    print("UFW configuration updated.")
    setup_nat()
    print("NAT setup completed.")

    print("Script completed!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os
import subprocess
import json

def is_root():
    return os.geteuid() == 0

def is_jq_installed():
    try:
        subprocess.run(["jq", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except:
        return False

def install_jq():
    subprocess.run(["apt-get", "update"], check=True)
    subprocess.run(["apt-get", "install", "-y", "jq"], check=True)

def update_docker_config():
    # Read the original data first
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
    subprocess.run(["systemctl", "restart", "docker"], check=True)

def main():
    if not is_root():
        print("Please run the script as root or with sudo.")
        return

    if not is_jq_installed():
        print("jq is not installed. Installing now...")
        install_jq()

    update_docker_config()
    print("/etc/docker/daemon.json has been updated.")

    restart_docker()
    print("Docker daemon has been restarted.")

if __name__ == "__main__":
    main()

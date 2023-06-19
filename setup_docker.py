#!/usr/bin/env python3
import subprocess
import shutil
import os
import requests
import socket
import sys

# Function to check for sudo access
def check_sudo_access():
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(['sudo', '-n', 'true'], stdout=devnull, stderr=devnull)
        print("User has sudo access.")
    except subprocess.CalledProcessError:
        print("User", os.environ['USER'], "does not have sudo access.")
        sys.exit(1)
        
# Function to check for the presence of curl
def check_curl():
    if not shutil.which('curl'):
        print("Curl is not found. Installing curl...")
        try:
            subprocess.run(['sudo', 'apt', 'install', '-y', 'curl'], check=True)
            print("Curl has been installed.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during curl installation: {e}")
            sys.exit(1)
    else:
        print("Curl is already installed.")

# Define a function to get the IP address of the current machine
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

# Define a function to install Docker Compose
def install_docker_compose():
    response = requests.get("https://api.github.com/repos/docker/compose/releases/latest")
    if response.ok:
        latest_version = response.json()['tag_name']
        print(f"Latest version of Docker Compose: {latest_version}")
        if shutil.which('docker-compose'):
            current_version = subprocess.run(['docker-compose', 'version', '--short'], capture_output=True, text=True).stdout.strip()
            if latest_version == current_version:
                print("Docker Compose is already up to date.")
                return
        uname = os.uname()
        url = f"https://github.com/docker/compose/releases/download/{latest_version}/docker-compose-{uname.sysname}-{uname.machine}"
        try:
            subprocess.run(['sudo', 'curl', '-L', url, '-o', '/usr/local/bin/docker-compose'], check=True)
            subprocess.run(['sudo', 'chmod', '+x', '/usr/local/bin/docker-compose'], check=True)
            print(f"Docker Compose has been updated to version {latest_version}.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during Docker Compose installation: {e}")
            sys.exit(1)
    else:
        print("Failed to get the latest version of Docker Compose from GitHub API.")
        sys.exit(1)

# Function to check if the user is already in the docker group
def is_user_in_docker_group():
    username = os.getlogin()
    groups = subprocess.run(['groups', username], capture_output=True, text=True).stdout.strip()
    return 'docker' in groups.split()

# Function to add the user to the docker group
def add_user_to_docker_group():
    username = os.getlogin()
    if is_user_in_docker_group():
        print(f"User '{username}' is already a member of the 'docker' group.")
    else:
        try:
            subprocess.run(['sudo', 'usermod', '-aG', 'docker', username], check=True)
            print(f"User '{username}' has been added to the 'docker' group.")
            print("Please log out and log back in for the changes to take effect.")
            sys.exit()
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while adding the user to the docker group: {e}")
            sys.exit(1)

# Function to install Portainer service
def install_portainer_service():
    portainer_dir = os.path.expanduser('~/AppData/Portainer')
    os.makedirs(portainer_dir, exist_ok=True)

    if not os.path.exists(os.path.join(portainer_dir, 'docker-compose.yml')):
        # Create docker-compose.yml file for Portainer
        with open(os.path.join(portainer_dir, 'docker-compose.yml'), 'w') as f:
            f.write("""
version: '3'
services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./portainer-data:/data
    ports:
      - 8000:8000
      - 9000:9000
""")
    print("Portainer docker-compose file has been created.")

    while True:
        run_portainer = input("Do you want to start the Portainer service now? [y/n]: ").lower()
        if run_portainer in ['y', 'n']:
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    if run_portainer == 'y':
        try:
            # Start Portainer service using docker-compose
            subprocess.run(['docker-compose', '-f', os.path.join(portainer_dir, 'docker-compose.yml'), 'up', '-d'], check=True)
            print("Portainer service has been started.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while starting the Portainer service: {e}")
            sys.exit(1)

# Function to install Portainer agent
def install_portainer_agent():
    portainer_agent_dir = os.path.expanduser('~/AppData/PortainerAgent')
    os.makedirs(portainer_agent_dir, exist_ok=True)

    if not os.path.exists(os.path.join(portainer_agent_dir, 'docker-compose.yml')):
        # Create docker-compose.yml file for Portainer agent
        with open(os.path.join(portainer_agent_dir, 'docker-compose.yml'), 'w') as f:
            f.write("""
version: '3'

services:
  portainer_agent:
    image: portainer/agent:latest
    restart: always
    ports:
      - 9001:9001
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /var/lib/docker/volumes:/var/lib/docker/volumes
""")
    print("Portainer agent docker-compose file has been created.")

    while True:
        run_portainer_agent = input("Do you want to run the Portainer agent now? [y/n]: ").lower()
        if run_portainer_agent in ['y', 'n']:
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    if run_portainer_agent == 'y':
        try:
            # Start Portainer agent using docker-compose
            subprocess.run(['docker-compose', '-f', os.path.join(portainer_agent_dir, 'docker-compose.yml'), 'up', '-d'], check=True)
            print("Portainer agent has been started.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while starting the Portainer agent: {e}")
            sys.exit(1)
# Call the check_sudo_access function
check_sudo_access()

# Call the check_curl function
check_curl()

# Get the IP address of the current machine
ip_address = get_ip_address()

# Check if Docker is already installed
if not shutil.which('docker'):
    # Install Docker using get.docker.com script
    try:
        subprocess.run(['curl', '-fsSL', 'https://get.docker.com', '-o', 'get-docker.sh'], check=True)
        subprocess.run(['sudo', 'sh', 'get-docker.sh'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during Docker installation: {e}")
        sys.exit(1)
else:
    print("Docker is already installed.")

# Add user to docker group
add_user_to_docker_group()

# Install Docker Compose
install_docker_compose()

# Check if the user wants to install Portainer or Portainer agent
while True:
    install_portainer = input("Do you want to install Portainer or Portainer agent? [p/a]: ").lower()
    if install_portainer in ['p', 'a']:
        break
    else:
        print("Invalid input. Please enter 'p' or 'a'.")

if install_portainer == 'p':
    # Install Portainer service
    install_portainer_service()
elif install_portainer == 'a':
    # Install Portainer agent
    install_portainer_agent()

# Clean up
while True:
    cleanup = input("Do you want to remove the get-docker.sh file? [y/n]: ").lower()
    if cleanup in ['y', 'n']:
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.")

if cleanup == 'y':
    try:
        os.remove('get-docker.sh')
        print("get-docker.sh file has been removed.")
    except OSError as e:
        print(f"Error occurred while removing get-docker.sh file: {e}")

while True:
    cleanup = input("Do you want to remove the old images and containers? [y/n]: ").lower()
    if cleanup in ['y', 'n']:
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.")

if cleanup == 'y':
    try:
        # Remove all stopped containers
        subprocess.run(['docker', 'container', 'prune', '-f'], check=True)

        # Remove all dangling images
        subprocess.run(['docker', 'image', 'prune', '-f'], check=True)

        print("Old images and containers have been removed.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while removing old images and containers: {e}")

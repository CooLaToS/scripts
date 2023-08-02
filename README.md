# Docker Scripts

This repository hosts various scripts to simplify and automate different tasks. One of the highlighted scripts is the Docker setup script.

## Docker Setup Script

This script is designed to automate the setup of Docker and related components on your machine. It allows you to install Docker, Docker Compose, and optionally set up Portainer or Portainer Agent.

### Prerequisites

- Python 3
- curl command-line tool
- sudo access

### Instructions

1. **Clone the repository**:
    
```zsh
git clone https://github.com/CooLaToS/scripts.git
```
    
2. **Navigate to the directory** where the script is located:
    
```zsh
cd scripts
```
    
3. **Execute the Docker Setup Script**:
       
```zsh
python3 setup_docker.py
```
    
4. Follow the prompts to install Docker, Docker Compose, and choose whether to install Portainer or Portainer Agent.
    
5. After the script completes, you will have Docker and the selected components set up on your machine.
    

### Script Details

The Docker Setup script performs the following tasks:

- Retrieves the IP address of the current machine.
- Checks if Docker is already installed and installs it if necessary.
- Adds the current user to the Docker group.
- Installs the latest version of Docker Compose if it is not already up to date.
- Offers the option to install either Portainer or Portainer Agent.
    - **Portainer**: Sets up Portainer as a Docker service and provides a web-based interface for managing Docker containers and resources.
    - **Portainer Agent**: Installs the Portainer Agent, allowing the machine to be managed by a Portainer instance.
- Offers the option to remove the `get-docker.sh` installation script and clean up old Docker images and containers.

### Docker Configuration Script

This script, named `fixdockerfw.py`, adjusts Docker configurations on an Ubuntu server, particularly updating the `/etc/docker/daemon.json` to set the `iptables` attribute.

#### Prerequisites

- Python 3.x
- Ubuntu or Debian-based Linux distributions.
- sudo or root permissions

#### Usage

1. Navigate to the scripts directory.
    
2. Ensure the script is executable:
      
```zsh
chmod +x fixdockerfw.py
```
    
3. Execute the script:
       
```zsh
sudo ./fixdockerfw.py
```
    

This script checks for the `jq` utility, creates a backup of the original Docker configuration, alters the `iptables` configuration, and restarts the Docker service.

---

**Disclaimer**: The scripts in this repository make changes to your system configuration. Use them at your own risk. It is recommended to review the scripts and understand the actions they perform before executing them.

If you encounter any issues or have questions about any script, feel free to reach out for assistance.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)



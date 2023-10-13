# # Docker Scripts

This repository hosts various scripts to simplify and automate different tasks. Highlighted scripts include the Docker setup script and the Docker configuration script.

## Docker Setup Script

This script is designed to automate the setup of Docker and related components on your machine. It allows you to install Docker, Docker Compose, and optionally set up Portainer or Portainer Agent.

### Prerequisites

- Python 3
- curl command-line tool
- sudo access
- pip
- pip install docker

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

## fixdockerfw.py Script

This script provides a consolidated solution for Docker network setup and system-level network configurations. It automates several tasks, such as:

### Features:

- **IP Forwarding** - Enables IP forwarding at the system level.
- **UFW Configuration** - Modifies UFW's default forward policy and allows rules for the Docker network.
- **NAT on iptables** - Sets up NAT rules for the Docker network.
- **Docker Configuration** - Updates Docker's `daemon.json` file to disable `iptables` and restarts the Docker daemon.
- **Docker Network Creation** - Ensures the existence of a Docker network named `CELLOCKNET`.

### Requirements:

- This script requires Python 3.
- The script must be run as root or using sudo.
- The `docker` Python package is required (install via `pip install docker`).

### Usage:

Navigate to the directory containing the script and run:

```zsh
sudo python3 fixdockerfw.py
```

---
## License

  

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

  

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

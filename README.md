# Docker Setup Script

This script is designed to automate the setup of Docker and related components on your machine. It allows you to install Docker, Docker Compose, and optionally set up Portainer or Portainer Agent.

## Prerequisites

- Python 3
- `curl` command-line tool
- `sudo` access

## Instructions

1. Clone the repository or copy the script to your local machine.
2. Open a terminal or command prompt and navigate to the directory where the script is located.
3. Run the script using the following command:

```bash
python3 setup_docker.py
```

4. Follow the prompts to install Docker, Docker Compose, and choose whether to install Portainer or Portainer Agent.
5. After the script completes, you will have Docker and the selected components set up on your machine.

## Script Details

The script performs the following tasks:

1. Retrieves the IP address of the current machine.
2. Checks if Docker is already installed and installs it if necessary.
3. Adds the current user to the Docker group.
4. Installs the latest version of Docker Compose if it is not already up to date.
5. Offers the option to install either Portainer or Portainer Agent.
- Portainer: Sets up Portainer as a Docker service and provides a web-based interface for managing Docker containers and resources.
- Portainer Agent: Installs the Portainer Agent, allowing the machine to be managed by a Portainer instance.
6. Offers the option to remove the `get-docker.sh` installation script and clean up old Docker images and containers.

Please note that this script assumes a Linux environment. It may need modifications to work on other operating systems.

**Disclaimer:** This script makes changes to your system configuration. Use it at your own risk. It is recommended to review the script and understand the actions it performs before executing it.

If you encounter any issues or have any questions, feel free to reach out for assistance.

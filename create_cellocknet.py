import docker

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

if __name__ == "__main__":
    create_docker_network()

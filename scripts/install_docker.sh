#!/usr/bin/env bash
set -euo pipefail

# Installer for Docker and Docker Compose on Ubuntu/Debian systems.
# Run this script with sudo:
#   sudo ./scripts/install_docker.sh
# After running, log out and log back in to apply the docker group membership.

if [[ $(id -u) -ne 0 ]]; then
  echo "This script must be run as root or with sudo."
  exit 1
fi

apt update
apt install -y ca-certificates curl gnupg lsb-release
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  > /etc/apt/sources.list.d/docker.list

apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker installation failed or docker is not in PATH."
  exit 1
fi

echo "Docker installed successfully."

groupadd -f docker
usermod -aG docker "$SUDO_USER"

echo "Docker group updated. After this script finishes, log out and back in or run 'newgrp docker'."

echo "To start the sample Docker environment, run: ./scripts/run_docker_and_tests.sh"

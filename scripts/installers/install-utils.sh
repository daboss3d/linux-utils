#!/bin/bash

# Update package list and upgrade installed packages
sudo apt update && sudo apt upgrade -y

# Install common utilities
Pkgs=(
    curl
    wget
    git
    unzip
    htop
    net-tools
    nfs-common
)

echo "Installing utility packages..."
for pkg in "${Pkgs[@]}"; do
    sudo apt install -y "$pkg"
done

# Clean up
sudo apt autoclean -y
sudo apt autoremove -y

echo "Utility installation complete!"

# Bat - a better cat - https://github.com/sharkdp/bat -> Versions https://github.com/sharkdp/bat/releases

#!/bin/bash

# Function to check if bat (batcat) is installed
is_bat_installed() {
  command -v bat >/dev/null 2>&1
}

# Check if "curl" is available as it's needed for downloading binaries.
if ! command -v curl > /dev/null; then
    echo "This script requires 'curl' to be installed. Please install curl and rerun this script."
    exit 1
fi
# Fetch the latest version of bat from GitHub releases page
LATEST_VERSION=$(curl -s https://api.github.com/repos/sharkdp/bat/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')

echo "Latest 'bat' version found: $LATEST_VERSION"

# Check if bat (batcat) is already installed
if is_bat_installed; then
    echo "'bat' (batcat) is already installed."
else
    echo "Installing 'bat' (batcat)..."

    # Download and install bat based on the OS type
    if [ "$(uname)" = "Darwin" ]; then
        brew install bat
    else
        curl -L https://github.com/sharkdp/bat/releases/download/${LATEST_VERSION}/bat_x86_64-unknown-linux-gnu.tar.gz --output bat.tar.gz
        tar xvfz bat.tar.gz
        sudo mv ./bat_linux_x86_64/* /usr/local/bin/
        rm -rf bat* bat.tar.gz
    fi

    # Check again if installation was successful
    if is_bat_installed; then
        echo "'bat' (batcat) installed successfully."
    else
        echo "Failed to install 'bat'. Please check your internet connection and try again later."
        exit 1
    fi
fi

# Create a symbolic link to use bat as the cat command
if [ -L /usr/bin/cat ] && [ "$(readlink /usr/bin/cat)" = "/usr/local/bin/bat" ]; then
    echo "'cat' is already linked to 'bat'."
else
    sudo ln -sf /usr/local/bin/bat /usr/bin/cat
    echo "Created a symbolic link: cat -> bat."
fi

echo "Script execution completed successfully."
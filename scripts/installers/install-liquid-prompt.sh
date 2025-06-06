#!/bin/bash

# Set script to exit on errors
set -e

# Function to check if command exists
command_exists() {
    type "$1" &> /dev/null;
}

# Install necessary packages prerequisites (git)
echo "Checking for git installation..."
if ! command_exists git; then
  echo "Git is not installed, installing it now..."
  sudo apt-get update && sudo apt-get install -y git || { echo "Failed to install git." >&2; exit 1; }
else
  echo "Git is already installed."
fi

# Define installation directory and repository URL
REPO_URL="https://github.com/liquidprompt/liquidprompt"
INSTALL_DIR="$HOME/.local/share"

# Create directory if not exists (optional)
if [ ! -d "$INSTALL_DIR" ]; then
  echo "Creating the installation directory: $INSTALL_DIR..."
  mkdir -p "$INSTALL_DIR"
else
  echo "Installation directory already exists."
fi

# Clone the repository into the specified directory
echo "Cloning Liquid Prompt from GitHub..."
git clone "$REPO_URL" "$INSTALL_DIR/liquidprompt"

# Add liquidprompt initialization to user shell configuration file (.bashrc)
SHELL_CONF="$HOME/.bashrc"
if grep -q "source $INSTALL_DIR/liquidprompt/liquidprompt.sh" "$SHELL_CONF"; then
  echo ".bashrc already updated with Liquid Prompt source line."
else
  echo "Adding Liquid Prompt initialization to .bashrc..."
  echo "source $INSTALL_DIR/liquidprompt/liquidprompt.sh" >> "$SHELL_CONF"
fi

# Apply the changes to the current shell session (optional)
echo "Applying changes to the current shell session..."
source "$SHELL_CONF"

echo "Installation of Liquid Prompt completed successfully."

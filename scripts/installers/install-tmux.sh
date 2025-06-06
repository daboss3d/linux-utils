#!/bin/bash

# Directory where configuration files are stored:
CONFIG_DIR="config/tmux"
TMUX_CONFIG="$CONFIG_DIR/.tmux.conf"

echo "Checking if tmux is installed..."

if ! command -v tmux &> /dev/null; then
  echo "tmux is not installed. Installing now..."
  # Use the appropriate package manager for your system.
  case "$(uname)" in
    Linux*)
      if [ -f /etc/debian_version ]; then
        sudo apt-get update && sudo apt-get install -y tmux
      elif [ -f /etc/redhat-release ]; then
        sudo yum install -y tmux
      else
        echo "Unsupported Linux distribution."
        exit 1
      fi
      ;;
    Darwin*)
      brew install tmux
      ;;
    *)
      echo "Unsupported OS: $(uname)"
      exit 1
      ;;
  esac

else
  echo "tmux is already installed."
fi

# Check if configuration directory exists and copy .tmux.conf to the home directory:
echo "Configuring tmux..."

if [ -f "$TMUX_CONFIG" ]; then
  cp $TMUX_CONFIG ~/.tmux.conf
  echo ".tmux.conf copied to home directory: ~/.tmux.conf"
else
  echo "Configuration file not found at:$TMUX_CONFIG. Skipping configuration."
fi

echo "Installation and configuration of tmux completed!"

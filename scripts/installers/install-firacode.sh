 #!/bin/bash

# Name of the font to install
FONTFNAME="FiraCode"
FONTURL="https://github.com/tonsky/FiraCode/releases/download/5.2/Fira_Code.zip"

# Temporary directory to store the downloaded file
TEMP_DIR=$(mktemp -d)

# Function to check if a package is installed and installing it if not
install_if_not_exists() {
    echo "Checking for ${FONTFNAME} fonts..."
    fc-list | grep -i "${FONTFNAME}" &>/dev/null

    # If fira code fonts are not found, install them.
    if [ $? -ne 0 ]; then
        echo "${FONTFNAME} fonts are not installed"
        download_and_install
    else
        echo "${FONTFNAME} fonts are already installed"
    fi
}

# Function to download and install Fira Code font
download_and_install() {
    # Downloading the zip file from GitHub
    echo "Downloading ${FONTFNAME} from $FONTURL..."
    wget -O "$TEMP_DIR/FiraCode.zip" "$FONTURL"

    if [ $? -ne 0 ]; then
        echo "Failed to download ${FONTFNAME} font"
        rm -rf "$TEMP_DIR"
        exit 1
    fi

    # Unzipping the downloaded file
    echo "Unpacking Fira Code fonts..."
    unzip "$TEMP_DIR/FiraCode.zip" -d "$TEMP_DIR"

    if [ $? -ne 0 ]; then
        echo "Failed to extract ${FONTFNAME} font"
        rm -rf "$TEMP_DIR"
        exit 1
    fi

    # Copying the fonts to user's font directory
    FONTDIR="${HOME}/.fonts"

    if [ ! -d "${FONTDIR}" ]; then
        mkdir -p "${FONTDIR}"
    fi

    cp "$TEMP_DIR/ttf/"*.ttf "${FONTDIR}/"

    # Updating font cache, making new fonts available to the system
    fc-cache -fv

    # Cleaning up
    rm -rf "$TEMP_DIR"
}

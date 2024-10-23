#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Define variables
REPO_URL="https://github.com/AsmSafone/RadioPlayerV3.git"
TARGET_DIR="/RadioPlayerV3"
REQUIREMENTS_FILE="$TARGET_DIR/requirements.txt"

# Function to print messages with a timestamp
function log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Start cloning the repository
log "Cloning the repository, please wait..."
git clone "$REPO_URL" "$TARGET_DIR"

# Install requirements
log "Installing requirements..."
cd "$TARGET_DIR"
pip3 install --upgrade -r "$REQUIREMENTS_FILE"

# Start the bot
log "Starting the bot, please wait..."
python3 main.py

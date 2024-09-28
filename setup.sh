#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if command_exists python; then
    echo "Python is installed."
else
    echo "Python is not installed. Please install Python from https://www.python.org/downloads/"
    exit 1
fi

# Check if jq is installed
if command_exists jq; then
    echo "jq is installed."
else
    echo "jq is not installed. Please install jq from https://stedolan.github.io/jq/download/"
    exit 1
fi

# Directory for the virtual environment
venv_dir="venv"

# Remove and recreate the virtual environment if activation script is missing
if [ ! -d "$venv_dir" ] || [ ! -f "$venv_dir/Scripts/activate" ] && [ ! -f "$venv_dir/bin/activate" ]; then
    echo "Creating a new virtual environment..."
    rm -rf "$venv_dir"
    python -m venv "$venv_dir"
    echo "Successfully created virtual environment at $venv_dir."
fi

# Activate the virtual environment
if [ -f "$venv_dir/Scripts/activate" ]; then
    source "$venv_dir/Scripts/activate"
elif [ -f "$venv_dir/bin/activate" ]; then
    source "$venv_dir/bin/activate"
else
    echo "Error: Virtual environment activation script not found."
    exit 1
fi

# Upgrade pip and install TinyTuya within the virtual environment
pip install --upgrade pip
pip install tinytuya

echo "TinyTuya has been installed successfully in the virtual environment."

# Run the TinyTuya wizard interactively
echo "Running TinyTuya wizard..."
echo "Please answer 'Y' to all prompts during the wizard."
python -m tinytuya wizard

# Check if snapshot.json was created
if [[ ! -f "snapshot.json" ]]; then
    echo "Error: snapshot.json not found. Ensure the TinyTuya wizard completed successfully."
    deactivate
    exit 1
fi

# Extract necessary information from snapshot.json using jq for local device info
device_id=$(jq -r '.devices[0].id' snapshot.json)
ip_address=$(jq -r '.devices[0].ip' snapshot.json)
local_key=$(jq -r '.devices[0].key' snapshot.json)

# Extract necessary information from tinytuya.json using jq for cloud info (if needed)
api_key=$(jq -r '.apiKey' tinytuya.json)
api_secret=$(jq -r '.apiSecret' tinytuya.json)
api_region=$(jq -r '.apiRegion' tinytuya.json)

# Ensure .env is not a directory before creating it as a file
if [ -d ".env" ]; then
    echo ".env is a directory, removing it..."
    rm -rf .env
fi

# Create .env file with local configuration parameters expected by main.py
echo "Creating .env file..."
cat <<EOL > ./.env
DEVICE_ID=$device_id
IP_ADDRESS=$ip_address
LOCAL_KEY=$local_key
VERSION=3.4  # Adjusted based on snapshot.json version info.
EOL

echo ".env file created successfully!"

# Deactivate the virtual environment
deactivate

echo "Setup complete. You can now run your application with Docker Compose."
#!/bin/bash

# Get the absolute path of the project directory
PROJECT_DIR=$(pwd)

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip3 install -r requirements.txt
deactivate

# Check if service file exists in systemd
if [ ! -f "/etc/systemd/system/druzhische-bot.service" ]; then
    echo "Installing service..."
    
    # Update the service file with the correct path (automatically replaces /path/to/druzhische-bot)
    echo "Configuring service with path: $PROJECT_DIR"
    sed "s|/path/to/druzhische-bot|$PROJECT_DIR|g" druzhische-bot.service > druzhische-bot.service.tmp
    mv druzhische-bot.service.tmp druzhische-bot.service
    
    # Copy the service file to systemd directory
    sudo cp druzhische-bot.service /etc/systemd/system/
    
    # Reload systemd to recognize the new service
    sudo systemctl daemon-reload
    
    # Enable the service to start on boot
    sudo systemctl enable druzhische-bot
    
    echo "Service installed."
fi

# Start the service
sudo systemctl start druzhische-bot
echo "Service started."
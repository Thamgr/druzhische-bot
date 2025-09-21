#!/bin/bash

# Pull the latest code
git pull

# Update dependencies in the virtual environment
if [ -d "venv" ]; then
    echo "Updating dependencies..."
    source venv/bin/activate
    pip3 install -r requirements.txt
    deactivate
fi

# Restart the service
./stop.sh
./start.sh
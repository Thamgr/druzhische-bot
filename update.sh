#!/bin/bash

# Pull the latest code
git pull

# Update dependencies in the virtual environment
if [ -d "venv" ]; then
    echo "Updating dependencies..."
    ./venv/bin/pip install -r requirements.txt
fi

# Restart the service
./stop.sh
./start.sh
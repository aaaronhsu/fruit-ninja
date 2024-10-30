#!/bin/bash

# Activate the virtual environment
source fruit_ninja/bin/activate

# Set the NODE_OPTIONS environment variable
export NODE_OPTIONS=--openssl-legacy-provider

# Set the FLASK_RUN_PORT environment variable
export FLASK_RUN_PORT=8000

# Set the FLASK_APP environment variable
export FLASK_APP=server.py

echo "Environment setup complete."

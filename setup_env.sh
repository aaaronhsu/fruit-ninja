#!/bin/bash
source fruit_ninja/bin/activate
export NODE_OPTIONS=--openssl-legacy-provider
export FLASK_RUN_PORT=8000
export FLASK_APP=server.py
echo "Environment setup complete!"

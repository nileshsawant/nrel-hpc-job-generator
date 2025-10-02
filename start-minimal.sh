#!/bin/bash

# Minimal startup script for network-challenged environments
echo "🚀 Starting NREL HPC Job Generator (Minimal Mode)..."

# Install only essential packages
python -m pip install --no-deps --no-cache-dir flask==3.0.0 werkzeug==3.0.1 jinja2==3.1.2

# Set environment variables
export FLASK_ENV=production
export PORT=${PORT:-5000}

echo "🌐 Starting on port $PORT..."
echo "📋 Once running, use the PORTS tab in VS Code to access the app"

# Start with minimal configuration
python -c "
import sys
sys.path.insert(0, '.')
from app import app
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=False)
"
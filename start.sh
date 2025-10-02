#!/bin/bash

echo "🚀 Starting NREL HPC Job Script Generator..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python installation
if ! command_exists python && ! command_exists python3; then
    echo "❌ Python not found. Please ensure Python is installed."
    exit 1
fi

# Use python3 if python is not available
PYTHON_CMD="python"
if ! command_exists python && command_exists python3; then
    PYTHON_CMD="python3"
fi

echo "🐍 Using Python: $($PYTHON_CMD --version)"

# Check if Flask is installed, install if needed
if ! $PYTHON_CMD -c "import flask" 2>/dev/null; then
    echo "📦 Installing Flask dependencies..."
    if [ -f "requirements.txt" ]; then
        $PYTHON_CMD -m pip install --no-cache-dir -r requirements.txt
    else
        $PYTHON_CMD -m pip install --no-cache-dir flask werkzeug jinja2
    fi
fi

# Check if port 5000 is available
if command_exists lsof && lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 5000 is busy, using port 5001..."
    export PORT=5001
    echo "🌐 App will be available at: http://localhost:5001"
else
    echo "🌐 App will be available at: http://localhost:5000"
fi

# Start the Flask app
echo "🔥 Starting Flask application..."
echo "📋 Once started, look for the 'PORTS' tab in VS Code and click the globe icon"
echo ""

$PYTHON_CMD app.py
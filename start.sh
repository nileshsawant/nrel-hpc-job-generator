#!/bin/bash

echo "🚀 Starting NREL HPC Job Script Generator..."

# Check if dependencies are installed
if [ ! -d ".venv" ] && [ ! -f "/usr/local/bin/flask" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if port 5000 is available
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 5000 is busy, using port 5001..."
    export PORT=5001
    echo "🌐 App will be available at: http://localhost:5001"
else
    echo "🌐 App will be available at: http://localhost:5000"
fi

# Start the Flask app
echo "🔥 Starting Flask application..."
python app.py
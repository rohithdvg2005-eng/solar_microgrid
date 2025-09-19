#!/bin/bash

echo "🚀 Solar Microgrid Streamlit Deployment"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✅ Python3 and pip3 are installed"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements-streamlit.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Start Streamlit application
echo "🌞 Starting Solar Microgrid Dashboard..."
echo "📍 Dashboard will be available at: http://localhost:8501"
echo "🔑 Demo OTP: 123456"
echo "📱 Use any phone number for login"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run deploy-streamlit.py --server.port 8501 --server.address 0.0.0.0

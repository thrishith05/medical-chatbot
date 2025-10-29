#!/bin/bash

echo "🏥 Medical Chatbot Frontend"
echo "=========================="
echo ""

# Check if backend is running
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ Backend API is running on port 8001"
else
    echo "⚠️  Backend API is not running"
    echo "   Please start it first with: python app.py"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🚀 Starting frontend server..."
echo ""

# Start the frontend server
python3 frontend_server.py


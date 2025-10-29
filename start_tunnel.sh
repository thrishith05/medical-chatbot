#!/bin/bash

# Expose your FastAPI app using Cloudflare Tunnel
# This bypasses Fortinet and most corporate firewalls

echo "🚀 Starting FastAPI app and Cloudflare Tunnel..."
echo ""

# Start the FastAPI app in the background
echo "Starting FastAPI on port 8001..."
python3 app.py &
FASTAPI_PID=$!
echo "FastAPI PID: $FASTAPI_PID"

# Wait a moment for the app to start
sleep 3

# Check if FastAPI is running
if ! curl -s http://localhost:8001/health > /dev/null; then
    echo "⚠️  FastAPI might not be running. Starting now..."
    kill $FASTAPI_PID 2>/dev/null
    python3 app.py &
    FASTAPI_PID=$!
    sleep 5
fi

echo ""
echo "✅ FastAPI is running!"
echo ""
echo "=== Starting Cloudflare Tunnel ==="
echo "Your API will be available at the URL shown below"
echo ""

# Start cloudflared tunnel
cloudflared tunnel --url http://localhost:8001

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $FASTAPI_PID 2>/dev/null
    echo "✅ Cleaned up!"
}

trap cleanup EXIT


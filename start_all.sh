#!/bin/bash

# Medical Chatbot - Start All Services
echo "🏥 Starting Medical Chatbot..."
echo ""

# Kill any existing servers
echo "Cleaning up existing servers..."
pkill -f "app.py" 2>/dev/null
pkill -f "frontend_server.py" 2>/dev/null
sleep 2

# Start API
echo "📡 Starting API server on port 8001..."
cd /Users/thrishithreddy/Desktop/HAC
python3 app.py > api.log 2>&1 &
API_PID=$!
echo "   API started (PID: $API_PID)"

# Wait for API
sleep 5

# Start Frontend
echo "🌐 Starting Frontend server on port 8080..."
python3 frontend_server.py > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend started (PID: $FRONTEND_PID)"

# Wait for servers
sleep 3

# Check status
echo ""
echo "✅ Checking services..."
if curl -s http://localhost:8001/health > /dev/null; then
    echo "   ✓ API: http://localhost:8001"
else
    echo "   ✗ API not responding"
fi

if curl -s http://localhost:8080/ > /dev/null; then
    echo "   ✓ Frontend: http://localhost:8080"
else
    echo "   ✗ Frontend not responding"
fi

echo ""
echo "🎉 Services are running!"
echo ""
echo "📍 URLs:"
echo "   Frontend: http://localhost:8080"
echo "   API: http://localhost:8001"
echo ""
echo "📝 To stop servers:"
echo "   pkill -f 'app.py'"
echo "   pkill -f 'frontend_server.py'"
echo ""


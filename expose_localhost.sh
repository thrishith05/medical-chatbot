#!/bin/bash

# Expose your local FastAPI app using localhost.run (SSH-based)
# This bypasses most corporate firewalls since it uses SSH port 22

echo "Starting local FastAPI app on port 8001..."
echo "Make sure you have SSH access configured"

# Method 1: Using localhost.run (recommended)
echo ""
echo "=== Option 1: Using localhost.run ==="
echo "Run this in a separate terminal:"
echo "ssh -R 80:localhost:8001 ssh@ssh6.localhost.run"
echo ""
echo "After running the above, you'll get a URL like:"
echo "https://random-name.localhost.run"
echo ""

# Method 2: Using serveo.net
echo "=== Option 2: Using serveo.net ==="
echo "Run this in a separate terminal:"
echo "ssh -R 80:localhost:8001 serveo.net"
echo ""

# Method 3: Using localhost.run without subdomain
echo "=== Option 3: Simple SSH Tunnel ==="
echo "ssh -R 8080:localhost:8001 ssh@ssh1.localhost.run"
echo ""

# To test if SSH tunnels work:
echo "=== Testing SSH access ==="
echo "Testing connection to localhost.run..."
if ssh -o ConnectTimeout=5 ssh@ssh1.localhost.run "echo 'SSH works!'" 2>/dev/null; then
    echo "✓ SSH tunnel should work!"
else
    echo "✗ SSH connection failed. You may need to:"
    echo "  - Check if port 22 is open in firewall"
    echo "  - Or use a different method below"
fi

echo ""
echo "After you get a tunnel URL, test your API with:"
echo "curl http://YOUR-URL/health"


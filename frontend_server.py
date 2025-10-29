#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend
"""

import http.server
import socketserver
import webbrowser
from pathlib import Path
import os

PORT = 8080
FRONTEND_DIR = Path(__file__).parent / 'frontend'

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow frontend to talk to API
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    os.chdir(FRONTEND_DIR)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Frontend server running at:")
        print(f"   http://localhost:{PORT}")
        print(f"   http://127.0.0.1:{PORT}")
        print(f"\n📝 Make sure your FastAPI backend is running on port 8001")
        print(f"   API URL: http://localhost:8001")
        print(f"\n⚠️  Press CTRL+C to stop the server\n")
        
        try:
            # Open browser automatically
            import time
            time.sleep(1)
            webbrowser.open(f'http://localhost:{PORT}')
        except Exception as e:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped")

if __name__ == "__main__":
    main()


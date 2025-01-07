#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from urllib.parse import parse_qs, urlparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
HOST = "localhost"
PORT = 8000

class ChatRequestHandler(BaseHTTPRequestHandler):
    """Custom request handler for our chat application"""

    def do_GET(self):
        """Handle GET requests"""
        # Parse the URL path
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == "/":
            # Serve the main page
            try:
                with open("templates/index.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, "File not found")
        
        elif parsed_path.path.startswith("/static/"):
            # Serve static files (CSS, JS)
            try:
                with open(parsed_path.path[1:], "rb") as f:
                    content = f.read()
                self.send_response(200)
                # Set content type based on file extension
                if parsed_path.path.endswith(".css"):
                    content_type = "text/css"
                elif parsed_path.path.endswith(".js"):
                    content_type = "text/javascript"
                else:
                    content_type = "text/plain"
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, "File not found")
        
        else:
            # Handle 404 for unknown paths
            self.send_error(404, "Path not found")

    def do_POST(self):
        """Handle POST requests"""
        # Get the size of the POST data
        content_length = int(self.headers.get("Content-Length", 0))
        
        # Read and parse the POST data
        post_data = self.rfile.read(content_length)
        
        try:
            # Try to parse as JSON
            data = json.loads(post_data.decode("utf-8"))
            
            # Handle different POST endpoints
            if self.path == "/api/messages":
                # Handle new message
                response_data = {"status": "success", "message": "Message received"}
                self.send_json_response(200, response_data)
            else:
                # Handle unknown endpoints
                self.send_json_response(404, {"status": "error", "message": "Endpoint not found"})
                
        except json.JSONDecodeError:
            # Handle invalid JSON
            self.send_json_response(400, {"status": "error", "message": "Invalid JSON"})

    def send_json_response(self, status_code, data):
        """Helper method to send JSON responses"""
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

def run_server():
    """Initialize and run the HTTP server"""
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, ChatRequestHandler)
    print(f"Server running at http://{HOST}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

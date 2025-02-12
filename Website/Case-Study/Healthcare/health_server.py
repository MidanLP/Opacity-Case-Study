import http.server
import socketserver
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

os.chdir(script_dir)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving HTTP on port {PORT}... from {script_dir}")
    # Run the server indefinitely
    httpd.serve_forever()
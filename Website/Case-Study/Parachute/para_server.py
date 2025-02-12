import http.server
import socketserver
import os

dir = os.path.dirname(os.path.abspath(__file__))

PORT = 8001

os.chdir(dir)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving HTTP on port {PORT} from {dir}...")
    # Run the server indefinitely
    httpd.serve_forever()


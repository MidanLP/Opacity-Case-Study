import http.server
import socketserver

# Set the port to 8000 (you can change it if needed)
PORT = 8000

# Create a handler that serves files from the current directory
Handler = http.server.SimpleHTTPRequestHandler

# Create the server with the specified port and handler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving HTTP on port {PORT}...")
    # Run the server indefinitely
    httpd.serve_forever()
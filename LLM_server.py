from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class QueryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL to get query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Print the full path and query parameters to terminal
        print(f"Received request: {self.path}")
        if query_params:
            print(f"Query parameters: {query_params}")
        
        # Send 200 OK response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
    
    def do_POST(self):
        # Handle POST requests similarly
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        print(f"Received POST request: {self.path}")
        print(f"Body: {body.decode('utf-8', errors='ignore')}")
        
        # Send 200 OK response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
    
    def log_message(self, format, *args):
        # Suppress default logging to keep output clean
        pass

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, QueryHandler)
    print(f"Server listening on port {port}...")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
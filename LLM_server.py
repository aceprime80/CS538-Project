from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from ollama import chat

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
        self.wfile.write(b'OK\n')
    
    def do_POST(self):
        # Handle POST requests
        content_length = int(self.headers.get('Content-Length', 0))
        content_type = self.headers.get('Content-Type', '')
        
        print(f"Received POST request: {self.path}")
        print(f"Content-Type: {content_type}")
        
        # Handle image upload endpoint
        if self.path == '/upload-image':
            body = self.rfile.read(content_length)
            
            # Save the image to disk
            filename = 'uploaded_image.jpg'
            
            # Try to determine file extension from content-type
            if 'image/png' in content_type:
                filename = 'uploaded_image.png'
            elif 'image/jpeg' in content_type or 'image/jpg' in content_type:
                filename = 'uploaded_image.jpg'
            elif 'image/gif' in content_type:
                filename = 'uploaded_image.gif'
            
            with open(filename, 'wb') as f:
                f.write(body)
            
            print(f"Image saved as: {filename}")
            print(f"Image size: {len(body)} bytes")
            
            response = chat(
                model='gemma3:12b',
                messages=[
                    {
                    'role': 'user',
                    'content': 'What is in this image? Be concise.',
                    'images': [filename],
                    }
                ],
            )
            print(response.message.content)
            # Send 200 OK response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = f'{{"status": "success", "filename": "{filename}", "description": "{response.message.content}", "size": {len(body)}}}\n'
            self.wfile.write(response.encode())
        else:
            # Handle other POST requests
            body = self.rfile.read(content_length)
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
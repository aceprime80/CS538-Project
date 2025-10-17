import http.server
import socketserver
import urllib.parse

PORT = 8000  # Choose a port

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':  # Handle requests to the root
            try:
                body = self.rfile.read().decode('utf-8')
                print(f"Received GET request body: {body}")
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"GET request body received and printed.\n")
            except Exception as e:
                print(f"Error processing request: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Error processing request.\n")
        else:
            super().do_GET() #Handle other requests normally.

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
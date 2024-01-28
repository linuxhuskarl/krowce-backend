import sys
from http.server import SimpleHTTPRequestHandler, HTTPServer


class GzipRequestHandler(SimpleHTTPRequestHandler):
    '''HTTPRequestHandler for gzip files'''

    def end_headers(self):
        '''Set Content-Encoding: gzip for gzipped files'''
        if self.path.endswith('.gz'):
            self.send_header('Content-Encoding', 'gzip')
        super().end_headers()

    def do_GET(self):
        '''Set Content-Encoding and Content-Type to gzipped files'''
        path = self.translate_path(self.path)
        if path.endswith('.js.gz'):
            with open(path, 'rb') as f:
                content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/javascript')
                self.add_cors_headers()  # Add CORS headers
                self.end_headers()
                self.wfile.write(content)
        elif path.endswith('.wasm.gz'):
            with open(path, 'rb') as f:
                content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/wasm')
                self.add_cors_headers()  # Add CORS headers
                self.end_headers()
                self.wfile.write(content)
        elif path.endswith('.gz'):
            with open(path, 'rb') as f:
                content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', self.guess_type(path))
                self.add_cors_headers()  # Add CORS headers
                self.end_headers()
                self.wfile.write(content)
        else:
            super().do_GET()

    def add_cors_headers(self):
        '''Add CORS headers to the response'''
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-type')


def serve(port: int):
    '''Run a local HTTP server'''
    httpd = HTTPServer(('0.0.0.0', port), GzipRequestHandler)
    print(f"Serving at http://0.0.0.0:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print(f'usage: {sys.argv[0]} [PORT]')
        port = int(sys.argv[1])
        serve(port)
    except Exception as e:
        print('Error:', e)

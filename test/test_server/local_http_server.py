import http.server
import socketserver
import threading
from pathlib import Path


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class LocalHttpServer:
    """Serve files from a local directory over HTTP for integration tests."""

    def __init__(self, directory, host="127.0.0.1", port=0):
        self.directory = Path(directory).resolve()
        self.host = host
        self.port = port

        def handler(*args, **kwargs):
            return http.server.SimpleHTTPRequestHandler(
                *args, directory=str(self.directory), **kwargs
            )

        self.httpd = ThreadedTCPServer((host, port), handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=3)

    @property
    def url(self):
        return f"http://{self.host}:{self.port}"

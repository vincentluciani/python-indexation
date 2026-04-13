"""Local HTTP server used by integration tests."""

import http.server
import socketserver
import threading
from pathlib import Path


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """A threaded TCP server that reuses the listening address."""

    allow_reuse_address = True


class LocalHttpServer:
    """Serve files from a local directory over HTTP for integration tests."""

    def __init__(self, directory, host="127.0.0.1", port=0):
        """Initialize the local HTTP server with directory, host, and port."""
        self.directory = Path(directory).resolve()
        self.host = host
        self.port = port

        def handler(*args, **kwargs):
            return http.server.SimpleHTTPRequestHandler(
                *args, directory=str(self.directory), **kwargs
            )

        self.httpd = ThreadedTCPServer((host, port), handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(
            target=self.httpd.serve_forever,
            daemon=True,
        )

    def start(self):
        """Start the local HTTP server thread."""
        self.thread.start()

    def stop(self):
        """Stop the local HTTP server and wait for the thread to finish."""
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=3)

    @property
    def url(self):
        """Return the base URL of the local HTTP server."""
        return f"http://{self.host}:{self.port}"

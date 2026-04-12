import pytest
import threading
import http.server
import socketserver
import requests
import os

# 1. Define the server logic
class MockServer:
    def __init__(self, port=8000, directory="tests/fixtures"):
        self.port = port
        self.directory = directory
        handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(
            *args, directory=self.directory, **kwargs
        )
        self.httpd = socketserver.TCPServer(("", self.port), handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()

# 2. Create the pytest fixture
@pytest.fixture(scope="session")
def local_server():
    # Setup: Start the server
    server = MockServer(port=8001)
    server.start()
    yield f"http://localhost:8001"  # Provide the base URL to the tests
    # Teardown: Stop the server
    server.stop()

# 3. Write your scraping test
def test_scraper_against_local(local_server):
    # 'local_server' here is the URL yielded by the fixture (http://localhost:8001)
    target_url = f"{local_server}/test_page.html"
    
    # Simulate your scraper's request
    response = requests.get(target_url)
    
    assert response.status_code == 200
    assert "Hello World" in response.text

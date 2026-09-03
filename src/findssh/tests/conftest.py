import pytest
import pytest_asyncio
import asyncio
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading


@pytest.fixture
def http_server_port():
    """Get an available port for test server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def mock_http_server(http_server_port):
    """Start a simple HTTP server for testing."""

    class SimpleHTTPHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Length", "13")
            self.end_headers()
            self.wfile.write(b"Test response")

        def log_message(self, format, *args):
            pass  # Suppress logging

    server = HTTPServer(("127.0.0.1", http_server_port), SimpleHTTPHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    yield http_server_port

    server.shutdown()


@pytest_asyncio.fixture
async def mock_http_server_async(http_server_port):
    """Async mock HTTP server using asyncio (alternative implementation)."""

    async def handle_http(reader, writer):
        """Handle HTTP connection by sending a response."""
        # Read the request (we don't need to parse it, just consume it)
        try:
            await reader.readuntil(b"\r\n\r\n")
        except asyncio.IncompleteReadError:
            pass
        except Exception:
            pass

        # Send HTTP response
        response = b"HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nTest response"
        writer.write(response)
        await writer.drain()
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass

    server = await asyncio.start_server(handle_http, "127.0.0.1", http_server_port)

    async def serve():
        async with server:
            await server.serve_forever()

    task = asyncio.create_task(serve())

    yield http_server_port

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    server.close()
    try:
        await server.wait_closed()
    except Exception:
        pass

"""
HTTP server detection utilities.

Provides functions to identify and validate HTTP service responses.
"""

import logging


def is_http_response(data: bytes) -> bool:
    """
    Check if response data contains an HTTP protocol indicator.

    Validates that the response starts with "HTTP/" which indicates
    a valid HTTP response (e.g., "HTTP/1.1 200 OK", "HTTP/1.0", etc.)

    Args:
        data: Raw bytes received from the server

    Returns:
        True if data appears to be an HTTP response, False otherwise
    """
    if not data:
        return False

    try:
        # Try to decode the first line
        lines = data.splitlines()
        if not lines:
            return False

        first_line = lines[0].decode("utf-8", errors="ignore").strip()
        return first_line.startswith("HTTP/")
    except Exception as err:
        logging.debug("Error checking HTTP response: %s", err)
        return False


def get_http_service(b: bytes) -> str | None:
    """
    Extract HTTP service banner/response from bytes.

    Returns the first line of the HTTP response, which typically contains
    the protocol version and status code (e.g., "HTTP/1.1 200 OK").

    Args:
        b: Raw bytes received from HTTP server

    Returns:
        First line of HTTP response if valid, None otherwise
    """
    if lines := b.splitlines():
        try:
            svc_txt = lines[0].decode("utf-8", errors="ignore").strip()
            if svc_txt.startswith("HTTP/"):
                return svc_txt
        except Exception:
            pass

    return None

"""
Local HTTPS proxy for Spotify Web API, designed for Mp3tag web sources.

This keeps your Spotify Client ID / Secret OUT of Mp3tag scripts and the repo.

Usage (example):
  export SPOTIFY_CLIENT_ID="your_client_id"
  export SPOTIFY_CLIENT_SECRET="your_client_secret"
  python3 spotify_proxy.py

Mp3tag can then talk to:
  https://localhost:8085/v1/search?...
  https://localhost:8085/v1/albums/{id}

The proxy fetches and caches an access token using the Client Credentials flow.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from ssl import wrap_socket
import base64
import json
import os
import time
from typing import Optional

import requests


CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_API_BASE = "https://api.spotify.com"
TOKEN_URL = "https://accounts.spotify.com/api/token"
PORT = int(os.environ.get("SPOTIFY_PROXY_PORT", "8085"))

session = requests.Session()

_access_token: Optional[str] = None
_token_expires_at: float = 0.0


def _get_access_token() -> str:
    """
    Fetch or refresh Spotify access token using Client Credentials flow.
    Token is cached until expiry.
    """
    global _access_token, _token_expires_at

    if not CLIENT_ID or not CLIENT_SECRET:
        raise RuntimeError(
            "SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set in the environment"
        )

    now = time.time()
    if _access_token and now < _token_expires_at - 60:
        return _access_token

    auth_header = base64.b64encode(
        f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")
    ).decode("ascii")
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    resp = session.post(TOKEN_URL, headers=headers, data=data, timeout=15)
    resp.raise_for_status()
    payload = resp.json()

    _access_token = payload.get("access_token")
    expires_in = int(payload.get("expires_in", 3600))
    _token_expires_at = now + expires_in

    if not _access_token:
        raise RuntimeError("Failed to obtain Spotify access token")

    return _access_token


def _forward_get(path: str) -> requests.Response:
    """
    Forward a GET request from Mp3tag to the Spotify Web API, handling auth.
    """
    url = SPOTIFY_API_BASE + path
    token = _get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    # You can add additional headers if needed
    resp = session.get(url, headers=headers, timeout=30)

    # If token expired unexpectedly, retry once
    if resp.status_code == 401:
        token = _get_access_token()
        headers["Authorization"] = f"Bearer {token}"
        resp = session.get(url, headers=headers, timeout=30)

    return resp


class SpotifyRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        # Less noisy logging
        return

    def do_GET(self) -> None:
        date = self.date_time_string(timestamp=None)
        print(f"{date} {self.path}")

        try:
            response = _forward_get(self.path)
        except Exception as exc:  # pylint: disable=broad-except
            print(f" -- ERROR -- {exc}")
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            body = {"error": "proxy_error", "message": str(exc)}
            self.wfile.write(json.dumps(body).encode("utf-8"))
            return

        self.send_response(response.status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response.content)

    def do_HEAD(self) -> None:
        self.send_response(200)
        self.end_headers()


def main() -> None:
    if not CLIENT_ID or not CLIENT_SECRET:
        raise SystemExit(
            "Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in the environment before running."
        )

    server = HTTPServer(("", PORT), SpotifyRequestHandler)
    # Reuse the same cert/key pattern as Apple Music proxy if present
    cert_file = os.environ.get("SPOTIFY_PROXY_CERT", "localhost.pem")
    key_file = os.environ.get("SPOTIFY_PROXY_KEY", "localhost.key")

    if os.path.exists(cert_file) and os.path.exists(key_file):
        server.socket = wrap_socket(
            server.socket, certfile=cert_file, keyfile=key_file, server_side=True
        )
        scheme = "https"
    else:
        # Fallback to plain HTTP if no cert; Mp3tag can still talk to http://localhost:PORT
        scheme = "http"

    print(f"Spotify proxy listening on {scheme}://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()

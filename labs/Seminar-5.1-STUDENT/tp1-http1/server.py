"""
TP1 — HTTP/1.1 File Transfer Server
======================================
Protocol stack: HTTP/1.1 → TCP → IP
Encryption    : None (traffic is visible in plain text in Wireshark)

Objective
---------
Implement Range Request handling (RFC 7233) so that the client can
fetch the data file chunk by chunk.

You will then observe each chunk request as a separate TCP connection
in Wireshark, with all headers readable in plain text.

Instructions
------------
Complete the 5 TODO sections below.
Do NOT modify any code outside the TODO sections.
Run the server with:  python server.py
Then in a second terminal: python client.py
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import os

# ──────────────────────────────────────────────────────────────────
# CONFIGURATION — Complete TODO 1
# ──────────────────────────────────────────────────────────────────

# TODO 1: Choose a port number for your HTTP server.
#         Rules: must be an integer greater than 1024 (no root required).
#         Suggested value: 8080
PORT = ????

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "data.txt")


# ──────────────────────────────────────────────────────────────────
# HTTP REQUEST HANDLER
# ──────────────────────────────────────────────────────────────────

class VideoHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        """Custom log: show method, path, and status code."""
        print(f"  [{self.command}] {self.path}  →  HTTP {args[1]}")

    def do_GET(self):
        """Route incoming GET requests."""
        if self.path == "/":
            self._serve_html()
        elif self.path == "/data":
            self._serve_data()
        else:
            self.send_error(404, "Not Found")

    # ── HTML page (provided — do not modify) ──────────────────────
    def _serve_html(self):
        html_path = os.path.join(os.path.dirname(__file__), "index.html")
        with open(html_path, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    # ── Data transfer — Complete TODOs 2 to 5 ────────────────────
    def _serve_data(self):
        """
        Serve the data file with Range request support (RFC 7233).

        The Python client fetches the file in chunks by sending GET requests
        with a 'Range' header asking for a specific portion of bytes:

            GET /data HTTP/1.1
            Range: bytes=0-1048575

        The server must:
          1. Read the Range header.
          2. Parse the start and end byte positions.
          3. Return only that portion of the file with status 206.
          4. Include a Content-Range header in the response.

        Complete the TODOs below to implement this mechanism.
        """
        file_size = os.path.getsize(DATA_PATH)

        # TODO 2: Read the "Range" header from the incoming HTTP request.
        #
        #   self.headers is a dict-like object containing all request headers.
        #   Use self.headers.get("HEADER_NAME") to read a header by name.
        #
        #   The header name is:  Range
        #   Example value:       bytes=0-1048575
        #
        range_header = self.headers.get("????")

        if range_header:
            # The browser is asking for a specific chunk of the video file.

            # TODO 3: Parse the start and end byte positions from range_header.
            #
            #   range_header looks like: "bytes=START-END"
            #
            #   Step A — Remove the "bytes=" prefix:
            #             use  range_header.replace("????", "")
            #
            #   Step B — Split the remaining "START-END" string on the dash "-":
            #             use  .split("????")   → gives a list ["START", "END"]
            #
            #   Step C — Convert START to an integer with int()
            #
            #   Step D — END may be empty (e.g., "bytes=1024-" means "from 1024
            #             to the end of the file"). Handle this case:
            #             if parts[1] is not empty → convert to int
            #             if parts[1] is empty     → use (file_size - 1)
            #
            range_spec = range_header.replace("????", "")
            parts = range_spec.split("????")
            start = int(parts[0])
            end   = int(parts[1]) if parts[1] else ???? - 1

            chunk_size = end - start + 1

            # TODO 4: Send the correct HTTP status code for a partial response.
            #
            #   200 OK          → full file is returned
            #   206 Partial Content → only part of the file is returned  ← use this one
            #
            self.send_response(????)

            # TODO 5: Fill in the Content-Range response header.
            #
            #   Format: "bytes START-END/TOTAL_FILE_SIZE"
            #   Example: if the file is 5 000 000 bytes and we return bytes 0–1048575:
            #            "bytes 0-1048575/5000000"
            #
            #   Replace the ???? below with the correct variable name for the total size.
            #
            self.send_header("Content-Range",
                             f"bytes {start}-{end}/????")
            self.send_header("Content-Length", str(chunk_size))
            self.send_header("Content-Type", "text/plain")
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()

            # Read and send the requested chunk (provided — do not modify)
            with open(DATA_PATH, "rb") as f:
                f.seek(start)
                self.wfile.write(f.read(chunk_size))

        else:
            # No Range header: serve the entire file (provided — do not modify)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(file_size))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            with open(DATA_PATH, "rb") as f:
                self.wfile.write(f.read())


# ──────────────────────────────────────────────────────────────────
# ENTRY POINT (provided — do not modify)
# ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), VideoHandler)
    print(f"\n  HTTP/1.1 server started")
    print(f"  Listening on: http://localhost:{PORT}")
    print(f"  Wireshark filter: tcp.port == {PORT}")
    print(f"\n  In a second terminal, run:  python client.py")
    print("  Press Ctrl+C to stop.\n")
    server.serve_forever()

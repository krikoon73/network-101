"""
TP1 — HTTP/1.1 File Transfer Server — SOLUTION
================================================
FOR INSTRUCTOR USE ONLY
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import os

# ── TODO 1 SOLUTION ──────────────────────────────────────────────
PORT = 8080
# Any port > 1024 is valid. 8080 is the conventional HTTP dev port.

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "data.txt")


class RequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"  [{self.command}] {self.path}  →  HTTP {args[1]}")

    def do_GET(self):
        if self.path == "/":
            self._serve_html()
        elif self.path == "/data":
            self._serve_data()
        else:
            self.send_error(404, "Not Found")

    def _serve_html(self):
        html_path = os.path.join(os.path.dirname(__file__), "..", "..", "tp1-http1", "index.html")
        with open(html_path, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _serve_data(self):
        file_size = os.path.getsize(DATA_PATH)

        # TODO 2 SOLUTION: "Range" is the exact HTTP header name
        range_header = self.headers.get("Range")

        if range_header:
            # TODO 3 SOLUTION:
            # range_header = "bytes=0-1048575"
            # → replace "bytes=" → "0-1048575"
            # → split "-"       → ["0", "1048575"]
            # → int()           → start=0, end=1048575
            range_spec = range_header.replace("bytes=", "")
            parts      = range_spec.split("-")
            start      = int(parts[0])
            end        = int(parts[1]) if parts[1] else file_size - 1

            chunk_size = end - start + 1

            # TODO 4 SOLUTION: 206 Partial Content
            self.send_response(206)

            # TODO 5 SOLUTION: Content-Range uses file_size as total
            self.send_header("Content-Range",
                             f"bytes {start}-{end}/{file_size}")
            self.send_header("Content-Length", str(chunk_size))
            self.send_header("Content-Type", "text/plain")
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()

            with open(DATA_PATH, "rb") as f:
                f.seek(start)
                self.wfile.write(f.read(chunk_size))

        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(file_size))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            with open(DATA_PATH, "rb") as f:
                self.wfile.write(f.read())


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), RequestHandler)
    print(f"\n  HTTP/1.1 server started")
    print(f"  Listening on: http://localhost:{PORT}")
    print(f"  Wireshark filter: tcp.port == {PORT}")
    print(f"\n  In a second terminal, run:  python client.py")
    print("  Press Ctrl+C to stop.\n")
    server.serve_forever()

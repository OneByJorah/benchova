# Minimal demo server for the benchova dashboard (stdlib only).
# Serves index.html + static assets and a demo /api/summary so the
# healthcheck and UI work without a live benchmark backend.
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("DASHBOARD_PORT", "8081"))
HOST = os.environ.get("DASHBOARD_HOST", "0.0.0.0")
ROOT = os.path.dirname(os.path.abspath(__file__))

DEMO_SUMMARY = {
    "status": "demo",
    "models_tested": 0,
    "note": "Demo data - connect OLLAMA_HOST to run real benchmarks.",
}

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/api/summary":
            body = json.dumps(DEMO_SUMMARY).encode()
            return self._send(200, "application/json", body)
        if path == "/healthz":
            return self._send(200, "text/plain", b"ok")
        if path == "/":
            path = "/index.html"
        safe = os.path.normpath(path).lstrip("/")
        full = os.path.join(ROOT, safe)
        if not full.startswith(ROOT) or not os.path.isfile(full):
            return self._send(404, "text/plain", b"not found")
        ctype = "text/html" if full.endswith(".html") else "text/plain"
        if full.endswith(".svg"):
            ctype = "image/svg+xml"
        try:
            with open(full, "rb") as f:
                return self._send(200, ctype, f.read())
        except OSError:
            return self._send(404, "text/plain", b"not found")

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    print(f"[benchova] serving {ROOT} on {HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()

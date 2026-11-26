"""Local presentation-only web interface; serves fictional tickets on localhost."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

os.environ.setdefault("OLLAMA_MODEL", "qwen2.5:1.5b")
os.environ.setdefault("RETRIEVAL_MODE", "semantic")

import simple_pipeline as pipeline

PAGE = Path(__file__).with_name("demo.html")


class Handler(BaseHTTPRequestHandler):
    def send_bytes(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/":
            self.send_bytes(404, b"Not found", "text/plain")
            return
        self.send_bytes(200, PAGE.read_bytes(), "text/html; charset=utf-8")

    def do_POST(self):
        if self.path != "/api/ask":
            self.send_bytes(404, b"Not found", "text/plain")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 8192:
                raise ValueError("invalid length")
            payload = json.loads(self.rfile.read(length))
            question = payload.get("question")
            if not isinstance(question, str) or not question.strip() or len(question) > 2000:
                raise ValueError("invalid question")
            result = pipeline.run_one(question.strip())
            safe = {key: result[key] for key in ("language", "decision", "send", "reason", "draft", "citations")}
            body = json.dumps(safe, ensure_ascii=False).encode("utf-8")
            self.send_bytes(200, body, "application/json; charset=utf-8")
        except (ValueError, TypeError, json.JSONDecodeError):
            self.send_bytes(400, b'{"error":"Invalid request"}', "application/json")
        except Exception:
            self.send_bytes(503, b'{"error":"The demo is unavailable. Please try again."}', "application/json")

    def log_message(self, format, *args):
        pass  # do not write ticket text to the server console


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("Demo running at http://127.0.0.1:8765 (Ctrl+C to stop)", flush=True)
    server.serve_forever()

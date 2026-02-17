from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        path = self.url().path
        if path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(self.get_home_page().encode("utf-8"))
            return

        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(self.get_not_found().encode("utf-8"))

    def get_home_page(self):
        with open("home.html", "r", encoding="utf-8") as file:
            return file.read()

    def get_not_found(self):
        return """
    <h1>404 Not Found</h1>
    <p>La pagina solicitada no existe.</p>
"""


if __name__ == "__main__":
    port = 8000
    server = HTTPServer(("localhost", port), WebRequestHandler)
    print(f"Starting server on port {port}")
    server.serve_forever()

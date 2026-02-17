from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


def load_contenido():
    datos = {}
    try:
        with open("home.html", "r", encoding="utf-8") as f:
            datos["/"] = f.read()
    except FileNotFoundError:
        datos["/"] = "<h1>Home no disponible</h1>"

    try:
        with open("1.html", "r", encoding="utf-8") as f:
            datos["/proyecto/1"] = f.read()
    except FileNotFoundError:
        datos["/proyecto/1"] = "<h1>Proyecto 1 no disponible</h1>"

    # Rutas de ejemplo para otros proyectos
    datos["/proyecto/2"] = """
<html>
  <body>
    <h1>Proyecto: 2</h1>
    <p>Contenido del proyecto 2 (en construcción)</p>
  </body>
</html>
"""
    datos["/proyecto/3"] = """
<html>
  <body>
    <h1>Proyecto: 3</h1>
    <p>Contenido del proyecto 3 (en construcción)</p>
  </body>
</html>
"""

    return datos


contenido = load_contenido()


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        path = self.url().path
        # Buscar en el diccionario de contenido
        if path in contenido:
            body = contenido[path]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            return

        # No encontrada: 404
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(self.get_not_found().encode("utf-8"))

    def get_not_found(self):
        return """
<html>
  <body>
    <h1>404 Not Found</h1>
    <p>La pagina solicitada no existe.</p>
  </body>
</html>
"""


if __name__ == "__main__":
    port = 8000
    server = HTTPServer(("localhost", port), WebRequestHandler)
    print(f"Starting server on port {port}")
    server.serve_forever()

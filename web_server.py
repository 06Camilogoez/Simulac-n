import http.server
import socketserver
import os
import webbrowser

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

def start_server():
    os.chdir(WEB_DIR)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"Servidor iniciado en: {url}")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")

if __name__ == "__main__":
    start_server()

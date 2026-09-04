import http.server
import functools
import socketserver

def http_server(HTTP_PORT):
    global httpd
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory="./website")
    httpd = socketserver.TCPServer(("", HTTP_PORT), Handler)
    print("Server at port: ", HTTP_PORT)
    httpd.serve_forever()


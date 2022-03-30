import json
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import urllib
from task5 import main

import jinja2
from jinja2 import Template

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
  server_address = ('', 9000)
  httpd = server_class(server_address, handler_class)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      httpd.server_close()

class HttpGetHandler(BaseHTTPRequestHandler):
    """Обработчик с реализованным методом do_GET."""

    def do_GET(self):
        from urllib.parse import urlparse

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.path == '/favicon.ico':
            return ''

        result = urlparse(self.path)
        query = result.query.split('=')[1].replace("+", " ")
        results = main.vector_search(query)

        with open("../task1/index.txt", 'r', encoding="utf-8") as file:
            meta = json.loads(file.read())

        links = []

        for item in results:

            l = dict(info=info(item, query), link=meta["../archive/" + item])

            links.append(l)
            # print(item, meta["../archive/" + item])



        site = 'dfssf'
        domen = 'fffff'

        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "template.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        outputText = template.render(links=links)

        # tm = Template("My site name is {{ site }}.{{ domen }}")
        # msg = tm.render()

        self.wfile.write(outputText.encode())
        # self.wfile.write('<title>Простой HTTP-сервер.</title></head>'.encode())
        # self.wfile.write('<body>Был получен GET-запрос.</body></html>'.encode())

def info(html_name, query):
    info = ''




    return info


if __name__ == '__main__':

    run(handler_class=HttpGetHandler)


    pass

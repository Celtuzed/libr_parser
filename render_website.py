from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json


if __name__ == '__main__':

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )

    with open("results/books_information.json", "r", encoding='utf8') as information:
        json_books_information = information.read()

    books_information = json.loads(json_books_information)
    template = env.get_template('template.html')

    rendered_page = template.render(
        books=books_information
    )
    with open("index.html", "w", encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

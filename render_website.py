from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import json


def on_reload():

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


if __name__ == '__main__':

    on_reload()

    server = Server()

    server.watch('template.html', on_reload)

    server.serve(root='.')

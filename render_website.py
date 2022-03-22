import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


COLUMNS_ON_PAGE = 2
LINES_ON_PAGE = 10


def on_reload():

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template('template.html')

    with open("results/books_information.json", "r", encoding='utf8') as information:
        books_information = json.load(information)

    chunked_books_information = list(chunked(books_information, COLUMNS_ON_PAGE))
    all_pages = list(chunked(chunked_books_information, LINES_ON_PAGE))
    pages_number = len(all_pages)

    for page_number, books_for_page in enumerate(all_pages, 1):

        rendered_page = template.render(
            books=books_for_page,
            this_page=page_number,
            pages_number=pages_number
        )
        with open(f"pages/index{page_number}.html", "w", encoding='utf8') as file:
            file.write(rendered_page)


if __name__ == '__main__':

    os.makedirs("pages", exist_ok=True)

    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')

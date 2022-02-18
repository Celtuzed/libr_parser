import argparse
import json
import os

from pprint import pprint

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse

from download_files import download_txt, download_image
from main_parser_logic import parse_book_page


def get_books_urls(args):

    url = "http://tululu.org/"
    books_urls = []

    for page in range(args.start_page, args.end_page):

        category_url = f"http://tululu.org/l55/{page}"

        response = requests.get(category_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        books_selector = "table.d_book"
        book_selector = "a"
        books_soup = soup.select(books_selector)
        books = [book.select_one(book_selector)['href'] for book in books_soup]
        for book in books:
            books_urls.append(urljoin(url, book))

    return(books_urls)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Этот код нужен для парсинга онлайн библиотеки,\
                         а также скачиванию книг и картинок.'
    )

    parser.add_argument(
            '-sp', '--start_page',
            default=1,
            help='С какой страницы начинать парсить',
            type=int
                        )
    parser.add_argument(
            '-ep', '--end_page',
            default=2,
            help='До какой страницы будет парсить(включительно)',
            type=int
                        )

    parser.add_argument(
            '-jp', '--json_path',
            default='results',
            help='Указать свой путь к *.json файлу с результатами.'
    )
    parser.add_argument(
            '-df', '--dest_folder',
            default='results',
            help='Путь у каталогу с результатами парсинга: картинками, книгами и JSON.'
                        )

    parser.add_argument(
            '-si', '--skip_imgs',
            action='store_true',
            help='Не скачивать картинки.'
                        )
    parser.add_argument(
            '-st', '--skip_txt',
            action='store_true',
            help='Не скачивать книги.'
                        )
    args = parser.parse_args()

    dest_folder = args.dest_folder
    books_folder = os.path.join(dest_folder, "books")
    images_folder = os.path.join(dest_folder, "images")
    json_folder = args.json_path

    os.makedirs(dest_folder, exist_ok=True)
    os.makedirs(books_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(json_folder, exist_ok=True)

    books_urls = get_books_urls(args)
    books_information = []

    for book_url in books_urls:

        book_id = sanitize_filename(urlparse(book_url).path)[1:]

        params = {
            "id": book_id
        }
        url = "https://tululu.org/txt.php"

        try:

            book_information = parse_book_page(book_id)

            if not args.skip_txt:
                book_path = download_txt(url, params, book_information['book_name'], books_folder, book_id)
            else:
                book_path = None

            if not args.skip_imgs:
                img_path = download_image(book_information, book_information['book_name'], images_folder)
            else:
                img_path = None

            books_information.append({
                "title": book_information['book_name'],
                "author": book_information['author_name'],
                "img_scr": img_path,
                "book_path": book_path,
                "comments": book_information['comments']
            })

        except requests.exceptions.HTTPError:
            print(f"Не удалось скачать книгу с id = {book_id}")

    with open(os.path.join(args.json_path, "books_information.json"), "a", encoding='utf8') as file:
        json.dump(books_information, file, ensure_ascii=False)

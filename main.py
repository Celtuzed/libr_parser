import os
import argparse

import requests

from download_files import download_txt, download_image
from main_parser_logic import parse_book_page


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Этот код нужен для парсинга онлайн библиотеки,\
                         а также скачиванию книг и картинок.'
    )
    parser.add_argument(
            '-si', '--start_id',
            default=1,
            help='С какой книги начинать парсить',
            type=int
                        )
    parser.add_argument(
            '-ei', '--end_id',
            default=10,
            help='До какой книги будет парсить(включительно)',
            type=int
                        )
    args = parser.parse_args()

    books_folder = "books"
    os.makedirs(books_folder, exist_ok=True)
    images_folder = "images"
    os.makedirs(images_folder, exist_ok=True)

    for book_id in range(args.start_id, args.end_id):

        params = {
            "id": book_id
        }
        url = "https://tululu.org/txt.php"

        try:
            book_information = parse_book_page(book_id)
            filename = book_information['book_name']

            download_txt(url, params, filename, books_folder, book_id)
            download_image(book_information, filename, images_folder)
        except requests.exceptions.HTTPError:
            print(f"Не удалось скачать книгу с id = {book_id}")

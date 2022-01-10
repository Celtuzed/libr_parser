import os

import requests
from pathvalidate import sanitize_filename
from urllib.parse import urlsplit, unquote


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_txt(url, params, filename, books_folder, book_id):
    upgraded_filename = f"{book_id} {sanitize_filename(filename)}"
    response = requests.get(url, params)
    response.raise_for_status()
    check_for_redirect(response)
    path = os.path.join(books_folder, upgraded_filename)
    with open(f'{path}.txt', 'wt') as file:
        file.write(response.text)


def download_image(book_information, filename, images_folder):
    splited_link = urlsplit(book_information['image_link'])
    filename = unquote(splited_link.path.split('/')[2])
    response = requests.get(book_information['image_link'])
    response.raise_for_status()
    check_for_redirect(response)
    path = os.path.join(images_folder, filename)
    with open(path, 'wb') as file:
        file.write(response.content)

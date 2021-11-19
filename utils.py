import os

import requests
from pathvalidate import sanitize_filename
from urllib.parse import urlsplit, unquote


def check_for_redirect(response):
    if response.history:
        raise MyException('An HTTP error occurred.')


def download_txt(url, filename, books_folder, book_id):
    upgraded_filename = f"{book_id} {sanitize_filename(filename)}"
    response = requests.get(url)
    response.raise_for_status()
    path = os.path.join(books_folder, upgraded_filename)
    with open(f'{path}.txt', 'wb') as file:
        file.write(response.content)


def download_image(image_link, filename, images_folder, book_id):
    upgraded_filename = f"{book_id} {sanitize_filename(filename)}"
    splited_link = urlsplit(image_link)
    filename = unquote(splited_link.path.split('/')[2])
    response = requests.get(image_link)
    response.raise_for_status()
    path = os.path.join(images_folder, filename)
    with open(path, 'wb') as file:
        file.write(response.content)

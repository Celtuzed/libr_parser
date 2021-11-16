import os

import requests
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise MyException('An HTTP error occurred.')


def download_txt(url, filename, folder, book_id):
    response = requests.get(url)
    response.raise_for_status()
    path = os.path.join(folder, sanitize_filename(filename))
    with open(f'{path}.txt', 'wb') as file:
        file.write(response.content)

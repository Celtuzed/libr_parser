import os

import requests
from bs4 import BeautifulSoup

from utils import download_txt, check_for_redirect


def parse_html(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text
    book_name = title_text.split('::')[0].strip()
    return book_name

if __name__ == '__main__':

    folder = "books"
    os.makedirs(folder, exist_ok=True)

    for book_id in range(1, 11):

        url = f"https://tululu.org/txt.php?id={book_id}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            filename = parse_html(book_id)
            download_txt(url, filename, folder, book_id)
        except:
            print()

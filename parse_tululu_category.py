import requests
import json
import os

from pprint import pprint
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse

from download_files import download_txt, download_image
from main_parser_logic import parse_book_page


def get_books_urls():

    url = "http://tululu.org/"
    books_urls = []

    for page in range(5):

        category_url = f"http://tululu.org/l55/{page}"

        response = requests.get(category_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        books_soup = soup.find_all('table', class_='d_book')
        books = [book.find('a')['href'] for book in books_soup]
        for book in books:
            books_urls.append(urljoin(url, book))

    return(books_urls)

if __name__ == '__main__':

    books_folder = "books"
    os.makedirs(books_folder, exist_ok=True)
    images_folder = "images"
    os.makedirs(images_folder, exist_ok=True)

    books_urls = get_books_urls()
    books_information = []

    for book_url in books_urls:

        book_id = sanitize_filename(urlparse(book_url).path)[1:]

        params = {
            "id": book_id
        }
        url = "https://tululu.org/txt.php"

        try:

            book_information = parse_book_page(book_id)
            img_path = download_image(book_information, book_information['book_name'], images_folder)
            book_path = download_txt(url, params, book_information['book_name'], books_folder, book_id)

            books_information.append({
                "title": book_information['book_name'],
                "author": book_information['author_name'],
                "img_scr": img_path.replace('\\', '/'),
                "book_path": f"{book_path}.txt".replace('\\', '/'),
                "comments": book_information['comments']
            })

        except requests.exceptions.HTTPError:
            print(f"Не удалось скачать книгу с id = {book_id}")

    with open("books_information.json", "a", encoding='utf8') as file:
        json.dump(books_information, file, ensure_ascii=False)

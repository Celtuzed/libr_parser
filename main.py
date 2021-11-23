import os

import requests
from bs4 import BeautifulSoup

from utils import download_txt, download_image, check_for_redirect
from main_parser_logic import parse_html, get_comments, get_genres

if __name__ == '__main__':

    books_folder = "books"
    os.makedirs(books_folder, exist_ok=True)
    images_folder = "images"
    os.makedirs(images_folder, exist_ok=True)

    for book_id in range(1, 11):

        url = f"https://tululu.org/txt.php?id={book_id}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            filename, author_name, image_link = parse_html(book_id)
            download_txt(url, filename, books_folder, book_id)
            download_image(image_link, filename, images_folder, book_id)
        except:
            print()

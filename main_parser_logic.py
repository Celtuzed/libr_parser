import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from download_files import check_for_redirect


def parse_book_page(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')
    title_selector = "h1"
    title_text = soup.select(title_selector)[0].text
    book_name, author_name = title_text.split('::')

    comments_selector = "div.texts span"
    soup_comments = soup.select(comments_selector)
    comments = [comment.text for comment in soup_comments]

    genres_selector = "span.d_book a"
    soup_genres = soup.select(genres_selector)
    genres = [genre.text for genre in soup_genres]

    image_selector = ".bookimage img"
    title_image = soup.select(image_selector)[0]['src']
    image_link = urljoin(url, title_image)

    book_information = {
        "book_name": book_name.strip(),
        "author_name": author_name.strip(),
        "genres": genres,
        "comments": comments,
        "image_link": image_link
    }

    return book_information

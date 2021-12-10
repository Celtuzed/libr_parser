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
    title_tag = soup.find('h1')
    title_text = title_tag.text
    book_name, author_name = title_text.split('::')

    soup_comments = soup.find_all('div', class_='texts')
    comments = [comment.find('span').text for comment in soup_comments]

    soup_genres = soup.find_all('span', class_='d_book')
    genres = [genre.find('a').text for genre in soup_genres]

    title_image = soup.find(class_='bookimage').find('img')['src']
    image_link = urljoin(url, title_image)

    book_information = {
        "book_name": book_name.strip(),
        "author_name": author_name.strip(),
        "genres": genres,
        "comments": comments,
        "image_link": image_link
    }

    return book_information

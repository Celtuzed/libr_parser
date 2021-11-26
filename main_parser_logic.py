import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_book_page(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text
    book_name = title_text.split('::')[0].strip()
    author_name = title_text.split('::')[1].strip()

    comments = soup.find_all(class_='texts')
    normal_comments = []
    for comment in comments:
        normal_comments.append(comment.find('span').text)

    soup_genres = soup.find_all('span', class_='d_book')
    book_genres = []
    for soup_genre in soup_genres:
        genres = soup_genre.find_all('a')
    for genre in genres:
        book_genres.append(genre.text)

    book_information = {
        "book_name": book_name,
        "author_name": author_name,
        "genres": book_genres,
        "comments": normal_comments
    }

    title_image = soup.find(class_='bookimage').find('img')['src']
    image_link = urljoin(url, title_image)
    return book_information, image_link

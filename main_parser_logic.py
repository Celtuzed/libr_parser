import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_html(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text
    book_name = title_text.split('::')[0].strip()
    author_name = title_text.split('::')[1].strip()

    title_image = soup.find(class_='bookimage').find('img')['src']
    image_link = urljoin(url, title_image)
    return book_name, author_name, image_link

def get_comments(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    comments = soup.find_all(class_='texts')
    normal_comments = []
    for comment in comments:
        normal_comments.append(comment.find('span').text)
    return normal_comments

def get_genres(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    soup_genres = soup.find_all('span', class_='d_book')
    book_genres = []
    for soup_genre in soup_genres:
        genres = soup_genre.find_all('a')
    for genre in genres:
        book_genres.append(genre.text)
    return book_genres

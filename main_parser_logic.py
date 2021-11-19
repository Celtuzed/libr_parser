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

    title_image = soup.find(class_='bookimage').find('img')['src']
    image_link = urljoin(url, title_image)
    return book_name, image_link

import os

import requests

from bs4 import BeautifulSoup


def check_for_redirect(response):
    if response.history:
        raise MyException('An HTTP error occurred.')



def download_book(response, filename, folder):
    filename = f"book_{book_id}.txt"
    with open(f'{folder}\{filename}', 'wb') as file:
        file.write(response.content)


def parse_html(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text
    author_name = title_text.split('::')[1].strip()
    book_name = title_text.split('::')[0].strip()
    book_information = f"""
    Автор: {author_name}
    Название книги: {book_name}
    """
    print(book_information)

if __name__ == '__main__':

    folder = "books"
    os.makedirs(folder, exist_ok=True)

    for book_id in range(1, 11):

        url = f"https://tululu.org/txt.php?id={book_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            parse_html(book_id)
        except:
            print()

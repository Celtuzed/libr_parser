import os

import requests


def check_for_redirect(response):
    if response.history:
        raise MyException('An HTTP error occurred.')



def download_book(book_id):
    url = f"https://tululu.org/txt.php?id={book_id}"

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    filename = f"book_{book_id}.txt"
    with open(f'{folder}\{filename}', 'wb') as file:
        file.write(response.content)

if __name__ == '__main__':

    folder = "books"
    os.makedirs(folder, exist_ok=True)

    for book_id in range(1, 11):
        try:
            download_book(book_id)
        except:
            print()

import os

import requests

if __name__ == '__main__':
    folder = "books"
    os.makedirs(folder, exist_ok=True)

    for book_id in range(1, 11):
        url = f"https://tululu.org/txt.php?id={book_id}"

        response = requests.get(url)
        response.raise_for_status()

        filename = f"book_{book_id}.txt"
        with open(f'{folder}\{filename}', 'wb') as file:
            file.write(response.content)

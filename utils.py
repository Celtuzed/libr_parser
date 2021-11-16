import os

import requests
from pathvalidate import sanitize_filename

def download_txt(url, filename, folder, book_id):
    response = requests.get(url)
    response.raise_for_status()
    path = os.path.join(folder, sanitize_filename(filename))
    with open(f'{path}.txt', 'wb') as file:
        file.write(response.content)

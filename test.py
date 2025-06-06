### Just for having a look at what is fetched


import requests
from bs4 import BeautifulSoup

def fetch_page_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.get_text())

if __name__ == "__main__":
    url = "https://egedalkommune.dk/demokrati-og-indflydelse/vision-og-politikker/byudvikling-og-planlaegning/andre-planer-og-projekter/forum-veksoe"
    fetch_page_text(url)
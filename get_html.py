### Just for having a look at what is fetched

import requests
from bs4 import BeautifulSoup

URL = "https://egedalkommune.dk/demokrati-og-indflydelse/vision-og-politikker/byudvikling-og-planlaegning/andre-planer-og-projekter/forum-veksoe"

def fetch_meeting_links():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    
    container = soup.find("bui-base", class_="linkpicker")
    if not container:
        return []
    
    links = []
    for btn in container.find_all("bui-cta-button"):
        a_tag = btn.find("a", href=True)
        if a_tag:
            links.append((a_tag.text.strip(), a_tag["href"]))
    return links

if __name__ == "__main__":
    meeting_links = fetch_meeting_links()
    for title, href in meeting_links:
        print(title, href)

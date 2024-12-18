import requests
import string
from bs4 import BeautifulSoup
from urllib.parse import urljoin


base_url = "https://vimm.net/vault/"

def scrape_table(url):
    all_links = []

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        main_content = soup.find('main', class_='mainContent')
        if not main_content:
            print("main content not found!")
            return all_links

        table = main_content.find('table')
        if not table:
            print("table not found!")
            return all_links

        rows = table.find_all('tr')

        for row in rows:
            links = row.find_all('a', href=True)

            for link in links:
                href = link['href']
                if "?p=rating" not in href and "manual" not in href: # filter out pages we don't want
                    full_link = urljoin(url, href)
                    all_links.append(full_link)

        return all_links

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return all_links


def scrape_all_pages():
    all_links = []
    categories = ["number"] + list(string.ascii_uppercase)

    for c in categories: # number, A to Z
        page_number = 1
        while True:
            url = f"{base_url}?p=list&page={page_number}&action=filters&section={c}&system=NES&countries_all=1&countries[]=1&countries[]=2&countries[]=3&countries[]=35&countries[]=31&countries[]=4&countries[]=5&countries[]=6&countries[]=38&countries[]=7&countries[]=8&countries[]=9&countries[]=10&countries[]=11&countries[]=12&countries[]=13&countries[]=27&countries[]=33&countries[]=34&countries[]=14&countries[]=15&countries[]=16&countries[]=30&countries[]=17&countries[]=18&countries[]=40&countries[]=19&countries[]=28&countries[]=29&countries[]=20&countries[]=32&countries[]=37&countries[]=21&countries[]=22&countries[]=36&countries[]=23&countries[]=39&countries[]=41&countries[]=24&countries[]=25&countries[]=26&translated=1&prototype=1&demo=1&unlicensed=1&bonus=1&version=new&discs="
            print(f"Scraping: {base_url}NES/{c}/?page={page_number}")
            links = scrape_table(url)
            if not links:
                print(f"Nothing found on page {page_number} for category {c}")
                break

            all_links.append(links)
            page_number = page_number + 1

    return all_links

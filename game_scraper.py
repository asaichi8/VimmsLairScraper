import requests
import base64
from bs4 import BeautifulSoup


class GameScraper:
    def __init__(self):
        pass


    def scrape_html(self, url):
        print(f"Scraping info: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup

        except requests.exceptions.RequestException as e:
            print(f"Error scraping table! Error: {e}")
            return None


    # get the main content table containing title, hashes etc
    def extract_info_table(self, soup):
        try:
            main_content = soup.find('main', class_='mainContent')
            inner_main_content = main_content.find('div', class_='mainContent')
            table = inner_main_content.find('table')
            return table

        except AttributeError as e:
            print(f"Error extracting info table! Error: {e}")
            return None


    def extract_game_genie_table(self, soup):
        try:
            main_content = soup.find('main', class_='mainContent')
            tables = main_content.find_all('table')

            for table in tables:
                caption = table.find('caption')
                if caption and caption.get_text(strip=True) == "Official Game Genie Codes":
                    return table

            return None

        except AttributeError as e:
            print(f"Error extracting game genie table! Error: {e}")
            return None


    def extract_title(self, info_table):
        try:
            span = info_table.find('span', id="data-good-title")
            canvas = span.find('canvas', id="canvas2")
            base64_data = canvas.get('data-v')

            title = base64.b64decode(base64_data).decode('utf-8')
            return title
        except (base64.binascii.Error, UnicodeDecodeError, AttributeError) as e:
            print(f"Error extracting title! Error: {e}")
            return None


    def extract_md5_hash(self, info_table):
        try:
            rows = info_table.find_all('tr', class_='goodHash')

            for row in rows:
                td = row.find('td') # get first td
                if td.get_text(strip=True) == "MD5":
                    data_td = row.find('td', class_='ellipsis')
                    span = data_td.find('span', id="data-md5")
                    md5 = span.get_text(strip=True)

                    return md5

        except (IndexError, AttributeError) as e:
            print(f"Error extracting MD5 hash! Error: {e}")
            return None


    # returns the code, along with its description
    def extract_game_genie_codes(self, game_genie_table):
        codes = []

        try:
            rows = game_genie_table.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2 and cells[0] and cells[1]:
                    code = cells[0].get_text(strip=True)
                    description = cells[1].get_text(strip=True)

                    if code and description:
                        codes.append((code, description))

            return codes

        except AttributeError as e:
            print(f"Error extracting game genie codes! Error: {e}")
            return []

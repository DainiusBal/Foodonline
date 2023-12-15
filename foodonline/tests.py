import requests
from bs4 import BeautifulSoup
import re


class Scraping:
    def __init__(self, url):
        self.url = url
        self.source = requests.get(self.url).text
        self.soup = BeautifulSoup(self.source, "html.parser")
        print(self.source)

    def barbora_scrap(self):
        try:
            raw_price = self.soup.find('span', class_='b-product-price-current-number').text.strip()
            str_price = re.sub(r'[^\d,]', '', raw_price, re.MULTILINE)
            price = float(str_price.replace(',', '.'))
            return price
        except Exception as e:
            f'Error in barbora_scrap: {str(e)}'
            return None


url1 = 'https://www.barbora.lt/produktai/gazuotas-naturalus-mineralinis-vanduo-vytautas-1-5-l'

res = Scraping(url1).barbora_scrap()

print(res)
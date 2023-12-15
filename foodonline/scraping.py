import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urlparse
import logging


logger = logging.getLogger(__name__)


class Scraping:
    def __init__(self, url):
        self.url = url
        self.source = requests.get(self.url).text
        self.soup = BeautifulSoup(self.source, "html.parser")

    def barbora_scrap(self):
        try:
            raw_price = self.soup.find('span', class_='b-product-price-current-number').text.strip()
            str_price = re.sub(r'[^\d,]', '', raw_price, re.MULTILINE)
            price = float(str_price.replace(',', '.'))
            return price
        except Exception as e:
            logger.error(f'Error in barbora_scrap: {str(e)}')
            return None

    def scrap_product_name(self):
        try:
            name = self.soup.find('h1', class_='b-product-info--title').text.strip()
            return name
        except Exception as e:
            logger.error(f'Error in scrap_product_name: {str(e)}')
            return None

    def scrap_product_image(self):
        try:
            image_url = self.soup.find('div', class_='b-block-slider--slide').find()['src']
            response = requests.get(image_url)

            if response.status_code == 200:
                parsed_url = urlparse(image_url)
                filename = os.path.basename(parsed_url.path)
                image_path = os.path.join('foodonline', 'media', 'images', 'products', filename)
                image_path_db = os.path.join('images', 'products', filename)

                with open(image_path, 'wb') as image_file:
                    image_file.write(response.content)
                logger.info('Image download was successful')
                return image_path_db
            else:
                logger.error('Failed to download the image')
                return None
        except Exception as e:
            logger.error(f'Error in scrap_product_image: {str(e)}')
            return None

    def rimi_scrap(self):
        try:
            raw_price = self.soup.find('div', class_='price').text.strip()
            str_price_1 = re.search(r'(^\d\s+\d{2})', raw_price, re.MULTILINE)
            matched_text = str_price_1.group()
            str_price_2 = re.sub(r'[^\d,]', r'', matched_text, re.MULTILINE)
            price = float(str_price_2[:-2] + '.' + str_price_2[-2:])
            return price

        except Exception as e:
            logger.error(f'Error in rimi_scrap: {str(e)}')
            return None

    def aibe_scrap(self):
        try:
            raw_price = self.soup.find('span', {'id': 'our_price_display'}).text.strip()
            str_price = re.sub(r'[^\d,]', '', raw_price, re.MULTILINE)
            price = float(str_price.replace(',', '.'))
            return price

        except Exception as e:
            logger.error(f'Error in aibe_scrap: {str(e)}')
            return None

    def scrape_by_domain(url):
        try:
            scraper = Scraping(url)

            if 'barbora.lt' in url:
                return scraper.barbora_scrap()
            elif 'rimi.lt' in url:
                return scraper.rimi_scrap()
            elif 'aibesmaistas.lt' in url:
                return scraper.aibe_scrap()
            else:
                return None

        except Exception as e:
            logger.error(f'Error in scrape_by_domain: {str(e)}')
            return None











import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urlparse
import logging


logger = logging.getLogger(__name__)


class Scraping:

    def barbora_scrap(self):
        try:
            source = requests.get(self).text
            soup = BeautifulSoup(source, "html.parser")
            raw_price = soup.find('span', class_='b-product-price-current-number').text.strip()
            str_price = re.sub(r'[^\d,]', '', raw_price)
            price = float(str_price.replace(',', '.'))
            return price
        except Exception as e:
            logger.error(f'Error in barbora_scrap: {str(e)}')
            return None

    def scrap_product_name(self):
        try:
            source = requests.get(self).text
            soup = BeautifulSoup(source, "html.parser")
            name = soup.find('h1', class_='b-product-info--title').text.strip()
            return name
        except Exception as e:
            logger.error(f'Error in scrap_product_name: {str(e)}')
            return None

    def scrap_product_image(self):
        try:
            source = requests.get(self).text
            soup = BeautifulSoup(source, "html.parser")
            image_url = soup.find('div', class_='b-block-slider--slide').find()['src']
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
            source = requests.get(self).text
            soup = BeautifulSoup(source, "html.parser")

            name = soup.find('h1', class_='name').text.strip()
            raw_price = soup.find('div', class_='price').text.strip()
            str_price_1 = re.search(r'(^\d\s+\d{2})', raw_price, re.MULTILINE)
            matched_text = str_price_1.group()
            str_price_2 = re.sub(r'[^\d,]', r'', matched_text)
            price = float(str_price_2[:-2] + '.' + str_price_2[-2:])
            return price

        except Exception as e:
            logger.error(f'Error in rimi_scrap: {str(e)}')
            return None

    def aibe_scrap(self):
        try:
            source = requests.get(self).text
            soup = BeautifulSoup(source, "html.parser")

            name = soup.find('h1', {'itemprop': 'name'}).text.strip()
            raw_price = soup.find('span', {'id': 'our_price_display'}).text.strip()
            str_price = re.sub(r'[^\d,]', '', raw_price)
            price = float(str_price.replace(',', '.'))
            return price

        except Exception as e:
            logger.error(f'Error in aibe_scrap: {str(e)}')
            return None

    def scrape_by_domain(url):
        try:
            if 'barbora.lt' in url:
                return Scraping.barbora_scrap(url)
            elif 'rimi.lt' in url:
                return Scraping.rimi_scrap(url)
            elif 'aibesmaistas.lt' in url:
                return Scraping.aibe_scrap(url)
            else:
                return None

        except Exception as e:
            logger.error(f'Error in scrape_by_domain: {str(e)}')
            return None











from .models import Product, Price, Shop
from .scraping import Scraping
import logging


logger = logging.getLogger(__name__)


def update_product_prices():
    try:
        logger.info('Starting product price update...')
        products_with_urls = Product.objects.exclude(
            shop_url_1__isnull=True
        ).exclude(
            shop_url_2__isnull=True
        ).exclude(
            shop_url_3__isnull=True
        )

        for product in products_with_urls:
            logger.info(f'Updating prices for product: {product.name}')
            urls = [product.shop_url_1, product.shop_url_2, product.shop_url_3]
            prices = []

            for url in urls:
                price = Scraping.scrape_by_domain(url)
                prices.append(price)

            if len(prices) == 3:
                shop_1 = Shop.objects.get(name='BARBORA')
                shop_2 = Shop.objects.get(name='RIMI')
                shop_3 = Shop.objects.get(name='AIBĖ')

                price_shop_1 = Price.objects.get(product=product, shop=shop_1)
                price_shop_2 = Price.objects.get(product=product, shop=shop_2)
                price_shop_3 = Price.objects.get(product=product, shop=shop_3)

                price_shop_1.price = prices[0]
                price_shop_2.price = prices[1]
                price_shop_3.price = prices[2]

                product.update_last_update()
                try:
                    price_shop_1.save()
                    price_shop_2.save()
                    price_shop_3.save()
                    logger.info(f"Prices updated for product: {product.name}")
                except Exception as e:
                    logger.error(f"Failed to save prices for product {product.name}: {str(e)}")
    except Exception as ex:
        logger.error(f"Error in update_product_prices: {str(ex)}")
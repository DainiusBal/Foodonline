from django.contrib import admin
from .models import Shop, Product, Price, Category
from .forms import ProductAdminForm
from .scraping import Scraping
import logging


logger = logging.getLogger(__name__)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


class PriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'shop', 'price')
    list_filter = ('shop', 'price')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'category')
    fields = ('shop_url_1', 'shop_url_2', 'shop_url_3', 'category',)

    def save_model(self, request, obj, form, change):
        try:
            if obj.pk is None:
                shop_urls = [
                    ('BARBORA', form.cleaned_data['shop_url_1']),
                    ('RIMI', form.cleaned_data['shop_url_2']),
                    ('AIBĖ', form.cleaned_data['shop_url_3']),
                ]

                for shop_name, url in shop_urls:
                    price = Scraping.scrape_by_domain(url)
                    if price is not None:
                        shop, _ = Shop.objects.get_or_create(name=shop_name)
                        Price.objects.create(product=obj, shop=shop, price=price)

                first_url = shop_urls[0][1]
                name = Scraping(first_url).scrap_product_name()
                image_path = Scraping(first_url).scrap_product_image()

                if name:
                    obj.name = name
                if image_path:
                    obj.image = image_path
                    obj.save()

        except Exception as e:
            logger.error(f'Error in update_prices view: {str(e)}')


admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Category, CategoryAdmin)


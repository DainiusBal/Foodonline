from django.db import models
import datetime


class Shop(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=300, unique=True)
    shop_url_1 = models.URLField(blank=True, null=True, verbose_name="BARBORA", unique=True)
    shop_url_2 = models.URLField(blank=True, null=True, verbose_name="RIMI", unique=True)
    shop_url_3 = models.URLField(blank=True, null=True, verbose_name="AIBĖ", unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)

    def update_last_update(self):
        self.last_update = datetime.datetime.now()
        self.save()

    class Meta:
        unique_together = ('shop_url_1', 'shop_url_2', 'shop_url_3')

    def __str__(self):
        return self.name


class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.price}'



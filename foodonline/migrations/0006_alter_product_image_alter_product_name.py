# Generated by Django 4.2.7 on 2023-12-05 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodonline', '0005_remove_product_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]

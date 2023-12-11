from django.shortcuts import render, redirect
from .models import Product, Category, Price, Shop
from . import price_update
from .forms import ProductForm
from .scraping import Scraping
from django.contrib import messages
from django.core.paginator import Paginator


import logging

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def product_detail(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Exception as e:
        logger.error(f'Error in product_detail view: {str(e)}')

    return render(request, 'product_detail.html', {'product': product})


def all_products(request):
    try:
        categories = Category.objects.all()
        products = Product.objects.all()

        category_id = request.GET.get('category_id')
        if category_id:
            products = products.filter(category_id=category_id)

        query = request.GET.get('query')
        if query:
            products = products.filter(name__icontains=query)

        items_per_page = 5
        paginator = Paginator(products, items_per_page)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'all_products.html', {
            'categories': categories,
            'products': products,
            'selected_category_id': category_id,
            'page_obj': page_obj,
        })

    except Exception as e:
        logger.error(f'Error in all_product view: {str(e)}')


def add_to_cart(request, product_id):
    try:
        cart = request.session.get('cart', [])
        cart.append(product_id)
        request.session['cart'] = cart

    except Exception as e:
        logger.error(f'Error in add_to_cart view: {str(e)}')

    return redirect('all_products')


def basket(request):
    try:
        cart_product_ids = request.session.get('cart', [])
        cart_products = Product.objects.filter(id__in=cart_product_ids)

        shop_totals = {}

        for product in cart_products:
            for price in product.price_set.all():
                if price.shop.name not in shop_totals:
                    shop_totals[price.shop.name] = price.price
                else:
                    shop_totals[price.shop.name] += price.price

        context = {
            'cart_products': cart_products,
            'shop_totals': shop_totals,
        }

    except Exception as e:
        logger.error(f'Error in basket view: {str(e)}')

    return render(request, 'basket.html', context)


def remove_from_cart(request, product_id):
    try:
        cart = request.session.get('cart', [])

        if product_id in cart:
            cart.remove(product_id)
            request.session['cart'] = cart

    except Exception as e:
        logger.error(f'Error in remove_from_cart view: {str(e)}')

    return redirect('basket')


def search(request):
    try:
        query = request.GET.get('query')
        search_results = Product.objects.filter(name__icontains=query)
        return render(request, 'base.html', {'all_products': search_results, 'query': query})

    except Exception as e:
        logger.error(f'Error in search view: {str(e)}')


def update_prices(request):
    try:
        if request.method == 'POST':
            price_update.update_product_prices()
            messages.success(request, 'Kainos sėkmingai atnaujintos')
            return redirect('all_products')

    except Exception as e:
        logger.error(f'Error in update_prices view: {str(e)}')

    return render(request, 'all_products.html')


def add_product(request):
    try:
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                shop_urls = [
                    ('BARBORA', form.cleaned_data['shop_url_1']),
                    ('RIMI', form.cleaned_data['shop_url_2']),
                    ('AIBĖ', form.cleaned_data['shop_url_3']),
                ]

                name = Scraping.scrap_product_name(form.cleaned_data['shop_url_1'])
                if name:
                    obj.name = name

                obj.save()

                for shop_name, url in shop_urls:
                    price = Scraping.scrape_by_domain(url)
                    if price is not None:
                        shop, _ = Shop.objects.get_or_create(name=shop_name)
                        Price.objects.create(product=obj, shop=shop, price=price)

                for url in shop_urls:
                    url = shop_urls[0][1]
                image_path = Scraping.scrap_product_image(url)
                if image_path:
                    obj.image = image_path

                obj.save()
                messages.success(request, 'Produktas sėkmingai pridėtas')
                return redirect('all_products')  # Redirect after successful form submission
        else:
            form = ProductForm()

        return render(request, 'add_product.html', {'form': form})

    except Exception as e:
        logger.error(f'Error in add_product view: {str(e)}')
        messages.error(request, 'Produkto pridėjimo klaida')
        return render(request, 'add_product.html', {'form': ProductForm()})

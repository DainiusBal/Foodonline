from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.index, name='admin'),
    path('products', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('all_products', views.all_products, name='all_products'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('basket/', views.main_cart, name='basket'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('search/', views.search, name='search'),
    path('all_products/update_prices/', views.update_prices, name='update_prices'),
    path('add_product/', views.add_product, name='add_product'),
]
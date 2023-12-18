from django import forms
from .models import Product


class ProductAdminForm(forms.ModelForm):
    shop_url_1 = forms.URLField(label='BARBORA | URL')
    shop_url_2 = forms.URLField(label='RIMI | URL')
    shop_url_3 = forms.URLField(label='AIBE | URL')

    class Meta:
        model = Product
        fields = ['name', 'shop_url_1', 'shop_url_2', 'shop_url_3', 'category']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['shop_url_1', 'shop_url_2', 'shop_url_3', 'category']
        widgets = {
            'shop_url_1': forms.URLInput(attrs={'style': 'width: 100%'}),
            'shop_url_2': forms.URLInput(attrs={'style': 'width: 100%'}),
            'shop_url_3': forms.URLInput(attrs={'style': 'width: 100%'}),
        }



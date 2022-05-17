from django import forms

from .models import Product, Brand, Store


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'dimension', 'description', 'media_content', 'date_of_liquidation')


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('title',)


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('title', 'description', 'image')




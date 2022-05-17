from django import forms

from .models import Product, Brand


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('brand', 'title', 'dimension', 'description', 'media_content')


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('title', 'description', 'image')

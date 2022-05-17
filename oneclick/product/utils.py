from decimal import Decimal

from django.conf import settings
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Brand, BrandProduct, Product


def get_paginated_view(request, some_list):
    paginator = Paginator(some_list, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator


def get_product(request):
    products = {}
    post = request.POST
    for key, name in post.items():
        if key.startswith('nameProduct'):
            num = key.partition('_')[-1]
            products[name] = post[f'valueProduct_{num}']
    return products


def get_brand(request):
    brands = {}
    post = request.POST
    for key, name in post.items():
        if key.startswith('nameBrand'):
            num = key.partition('_')[-1]
            brands[name] = post[f'valueBrand_{num}']
    return brands


def save_product(request, form):
    with transaction.atomic():
        product = form.save(commit=False)
        product.author = request.user
        product.save()

        objs = []
        products = get_product(request)

        for name, quantity in products.items():
            product = get_object_or_404(Product, title=name)
            objs.append(
                BrandProduct(
                    product=product,
                    brand=brand,
                    quantity=Decimal(quantity.replace(',', '.'))
                )
            )

        BrandProduct.objects.bulk_create(objs)
        form.save_m2m()
        return product


def save_brand(request, form):
    with transaction.atomic():
        brand = form.save(commit=False)
        brand.author = request.user
        brand.save()

        objs = []
        brands = get_brand(request)
        for name in brands.items():
            brand = get_object_or_404(Brand, title=name)
            objs.append(
                BrandProduct(
                    brand=brand
                )
            )

        Brand.objects.bulk_create(objs)
        form.save_m2m()
        return brand


def edit_product(request, form, instance):
    with transaction.atomic():
        BrandProduct.objects.filter(product=instance).delete()
        return save_product(request, form)


def edit_brand(request, form, instance):
    with transaction.atomic():
        Brand.objects.filter(product=instance).delete()
        return save_brand(request, form)

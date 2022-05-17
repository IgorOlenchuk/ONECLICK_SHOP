from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Product, Brand
from .forms import ProductForm, BrandForm
from .utils import save_product, save_brand, edit_product, edit_brand, get_paginated_view

User = get_user_model()


def index(request):
    brands = Brand.objects.select_related(
        'title').distinct()
    products = Product.objects.select_related(
        'brand').distinct()

    page, paginator = get_paginated_view(request, brands, products)
    context = {
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'product/index.html', context)


@login_required
def product_new(request):
    form = ProductForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        product = save_product(request, form)

        return redirect(
            'product_view_slug', product_id=product.id, slug=product.slug
        )

    context = {'form': form}
    return render(request, 'product/form_product.html', context)


@login_required
def brand_new(request):
    form = BrandForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        brand = save_brand(request, form)

        return redirect(
            'brand_view_slug', product_id=brand.id, slug=brand.slug
        )

    context = {'form': form}
    return render(request, 'product/form_brand.html', context)


@login_required
def product_edit(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id)

    if not request.user.is_superuser:
        if request.user != product.author:
            return redirect(
                'product_view_slug', product_id=product.id, slug=product.slug
            )

    form = ProductForm(
        request.POST or None,
        files=request.FILES or None,
        instance=product
    )

    if form.is_valid():
        edit_product(request, form, instance=product)
        return redirect(
            'product_view_slug', product_id=product.id, slug=product.slug
        )

    context = {'form': form, 'product': product}
    return render(request, 'product/form_product.html', context)


@login_required
def brand_edit(request, brand_id, slug):
    brand = get_object_or_404(Brand, id=brand_id)

    if not request.user.is_superuser:
        if request.user != brand.author:
            return redirect(
                'brand_view_slug', brand_id=brand.id, slug=brand.slug
            )

    form = BrandForm(
        request.POST or None,
        files=request.FILES or None,
        instance=brand
    )

    if form.is_valid():
        edit_brand(request, form, instance=brand)
        return redirect(
            'brand_view_slug', brand_id=brand.id, slug=brand.slug
        )

    context = {'form': form, 'product': product}
    return render(request, 'product/form_product.html', context)


@login_required
def product_delete(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_superuser or request.user == product.author:
        product.delete()
    return redirect('index')


@login_required
def brand_delete(request, brand_id, slug):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.user.is_superuser or request.user == brand.author:
        brand.delete()
    return redirect('index')


def product_view_slug(request, product_id, slug):
    product = get_object_or_404(
        Product.objects.select_related('author'),
        id=product_id,
        slug=slug
    )
    context = {'product': product}
    return render(request, 'product/product_single_page.html', context)


def brand_view_slug(request, brand_id, slug):
    brand = get_object_or_404(
        Brand.objects.select_related('author'),
        id=brand_id,
        slug=slug
    )
    context = {'brand': brand}
    return render(request, 'product/brand_single_page.html', context)


def profile_view(request, username):
    author = get_object_or_404(User, username=username)
    author_brands = author.brands.distinct()
    author_products = author.products.distinct()
    page, paginator = get_paginated_view(request, author_brands, author_products)
    context = {
        'author': author,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'product/author_product.html', context)


def product_view_redirect(request, product_id):
    product = get_object_or_404(Product.objects.all(), id=product_id)
    return redirect('product_view_slug', product_id=product.id, slug=product.slug)


def brand_view_redirect(request, brand_id):
    brand = get_object_or_404(Brand.objects.all(), id=brand_id)
    return redirect('brand_view_slug', brand_id=brand.id, slug=brand.slug)

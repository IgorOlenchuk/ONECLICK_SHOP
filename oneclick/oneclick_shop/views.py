from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render

from product.models import Brand, Product
from product.utils import get_paginated_view

User = get_user_model()


def index(request):
    brands = Brand.objects.select_related(
        'store').distinct()

    page, paginator = get_paginated_view(request, brands)
    context = {
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'oneclick_shop/index.html', context)


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
    return render(request, 'oneclick_shop/author_product.html', context)

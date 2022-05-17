login_required
def purchases(request):
    products = request.user.purchases.all()
    return render(request, 'oneclick_shop/shop_list.html', {'products': products})


@login_required
def purchases_download(request):
    title = 'brand__product__title'
    dimension = 'brand__product__dimension'
    quantity = 'brand__product_amounts__quantity'

    products = request.user.purchases.select_related('brand').order_by(
        title).values(title, dimension).annotate(amount=Sum(quantity)).all()

    if not brands:
        return render(request, 'misc/400.html', status=400)

    text = 'Список покупок:\n\n'
    for number, product in enumerate(products, start=1):
        amount = product['amount']
        text += (
            f'{number}) '
            f'{brand[title]} - '
            f'{amount} '
        )

    response = HttpResponse(text, content_type='text/plain')
    filename = 'shopping_list.txt'
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response

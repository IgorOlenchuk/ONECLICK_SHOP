from django.urls import include, path


product_urls = [
    path('new/', product_new, name='product_new'),
    path('<int:product_id>/<slug:slug>/edit/', product_edit, name='product_edit'),
    path(
        '<int:product_id>/<slug:slug>/delete/',
        product_delete, name='product_delete'
    ),
    path(
        '<int:product_id>/<slug:slug>/',
        product_view_slug, name='product_view_slug'
    ),
    path(
        '<int:product_id>/', product_view_redirect,
        name='product_view_redirect'
    ),
]

urlpatterns = [
    path('', index, name='index'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('favorites/', favorites, name='favorites'),
    path('purchases/', include(purchases_urls)),
    path('product/', include(product_urls)),
    path('<str:username>/', profile_view, name='profile_view'),
]
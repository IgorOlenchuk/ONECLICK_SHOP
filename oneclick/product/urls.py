from django.urls import include, path

from .views import brand_new, brand_edit, brand_delete, brand_view_slug, brand_view_redirect

brand_urls = [
    path('new/', brand_new, name='brand_new'),
    path('<int:brand_id>/<slug:slug>/edit/', brand_edit, name='brand_edit'),
    path(
        '<int:brand_id>/<slug:slug>/delete/',
        brand_delete, name='brand_delete'
    ),
    path(
        '<int:brand_id>/<slug:slug>/',
        brand_view_slug, name='brand_view_slug'
    ),
    path(
        '<int:brand_id>/', brand_view_redirect,
        name='brand_view_redirect'
    ),
]

urlpatterns = [
    # path('subscriptions/', subscriptions, name='subscriptions'),
    # path('favorites/', favorites, name='favorites'),
    # path('purchases/', include(basket_urls)),
    path('brand/', include(brand_urls)),
]
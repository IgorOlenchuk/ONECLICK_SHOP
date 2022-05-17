from django.contrib import admin
from rest_framework.authtoken import views
from django.urls import path, include

#handler400 = 'blogs.views.page_bad_request'
#handler404 = 'blogs.views.page_not_found'
#handler500 = 'blogs.views.server_error'

urlpatterns = [
    # раздел администратора
    path('accounts/', include('users.urls')),
    path('accounts/', include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include('oneclick_shop.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/', include('api.urls')),
    path('product/', include('product.urls')),
    path('basket/', include('basket.urls')),
]
from django.contrib import admin

from .models import Brand, Product, Store, BrandsStore


class BrandsStoreInline(admin.TabularInline):
    model = BrandsStore
    min_num = 1
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'retail_price', 'wholesale_price', 'description', 'quantity', 'date_of_liquidation',
    )
    list_filter = ('brand__title', 'store__title', )
    search_fields = ('title',)
    ordering = ('-date_of_receipt', )


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('brand__title', 'title', )
    search_fields = ('title', )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    search_fields = ('^title', )

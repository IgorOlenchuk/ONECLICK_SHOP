from django.contrib import admin

from .models import Brand, Product, BrandProduct


class BrandProductInline(admin.TabularInline):
    model = BrandProduct
    min_num = 1
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (BrandProductInline, )
    list_display = (
        'id', 'title', 'retail_price', 'wholesale_price', 'description',
        'date_of_receipt', 'date_of_liquidation'
    )
    list_filter = ('brand', 'title')
    search_fields = ('brand__title', 'title',)
    autocomplete_fields = ('brand', )
    ordering = ('-date_of_receipt', )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('^title', )

from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models


class Brand(models.Model):
    title = models.CharField(
        'Наименование бренда',
        max_length=150,
        db_index=True
    )
    # Описание бренда
    description = models.TextField(max_length=140)
    # Логотип
    image = models.ImageField('Логотип', upload_to='brand/')

    class Meta:
        ordering = ('title', )
        verbose_name = 'бренд'
        verbose_name_plural = 'брендов'

    def __str__(self):
        return f'{self.title}, {self.description}'


class Product(models.Model):
    # Характеристики товара
    brand = models.ManyToManyField(
        Brand, through='BrandProduct'
    )
    title = models.CharField(
        'Название товарв',
        max_length=150,
        db_index=True
    )
    dimension = models.CharField('Единица измерения', max_length=10)
    # Описание
    description = models.TextField(max_length=140)
    # Фото и видео-контент в странице товара
    media_content = models.FileField('Медиа контент', upload_to='product/')
    # Цена товара, не меньше 0.01
    price = models.DecimalField(max_digits=12,
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))])
    # Даты поступления товаров
    date_of_receipt = models.DateTimeField(
        'Дата поступления',
        auto_now_add=True,
        db_index=True
    )
    date_of__liquidation = models.DateTimeField(
        'Дата ликвидации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-date_of_receipt', '-date_of__liquidation',)
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f'{self.brand}, {self.title}, {self.description}, {self.dimension}'


# Связта товара с Брэндом
class BrandProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='product_brand'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('product', 'brand'),
                name='unique_brand_product'
            )
        ]

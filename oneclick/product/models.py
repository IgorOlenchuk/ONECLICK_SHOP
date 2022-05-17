from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models


# Склад
class Store(models.Model):
    title = models.CharField(
        'Наименование склада',
        max_length=20,
        blank=False,
        db_index=True
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'склад'
        verbose_name_plural = 'склады'

    def __str__(self):
        return f'{self.title}'


class Brand(models.Model):
    title = models.CharField(
        'Наименование бренда',
        max_length=150,
        db_index=True
    )
    # Описание бренда
    description = models.TextField(max_length=140)
    # Логотип
    image = models.ImageField('Логотип', upload_to='brand/', blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        ordering = ('title',)
        verbose_name = 'бренд'
        verbose_name_plural = 'бренды'

    def __str__(self):
        return f'{self.title}, {self.description}'


# Товары
class Product(models.Model):
    # Характеристики товара
    title = models.CharField(
        'Название товарв',
        max_length=150,
        db_index=True
    )
    dimension = models.CharField('Единица измерения', max_length=10)
    # Описание
    description = models.TextField(max_length=140)
    # Фото и видео-контент в странице товара
    media_content = models.FileField('Медиа контент', upload_to='product/', blank=True)
    # Цена товара, не меньше 0.01
    retail_price = models.DecimalField(max_digits=12,
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))])
    wholesale_price = models.DecimalField(max_digits=12,
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))])
    # Даты поступления и ликвидации товаров
    date_of_receipt = models.DateTimeField(
        'Дата поступления',
        auto_now_add=True,
        db_index=True
    )
    date_of_liquidation = models.DateTimeField(
        'Дата ликвидации',
        auto_now_add=False,
        null=True,
        blank=True
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ('-date_of_receipt', )
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f'{self.title}, {self.description}, {self.dimension}'


# Связта товара с Брэндом и его складом
class BrandsStore(models.Model):
    brands = models.ForeignKey(Brand, on_delete=models.CASCADE)
    stores = models.ForeignKey(Store, on_delete=models.CASCADE)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('brands', 'stores'),
                name='unique_stores_brand'
            )
        ]

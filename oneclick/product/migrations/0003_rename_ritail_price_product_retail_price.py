# Generated by Django 3.2.13 on 2022-05-17 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20220517_1423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='ritail_price',
            new_name='retail_price',
        ),
    ]

# Generated by Django 5.1.1 on 2024-11-24 19:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_categories', '0001_initial'),
        ('products', '0002_product_condition'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product_categories.productcategory'),
        ),
    ]
# Generated by Django 5.1.1 on 2024-12-04 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_address_remove_customuser_city_customuser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/profile_pictures/'),
        ),
    ]

# Generated by Django 3.1.3 on 2020-11-14 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0003_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]

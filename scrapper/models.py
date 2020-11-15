from django.db import models

# Create your models here.
class Recipient(models.Model):
    """Email recipients"""
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.email


class Slug(models.Model):
    """Product slugs"""
    product_name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.product_name


class Product(models.Model):
    """Product and Price tracker"""
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    latest_price = models.FloatField(default=0)
    old_price = models.FloatField(default=0)
    url = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)

    def __str__(self):
        return self.name
from django.contrib import admin
from .models import Recipient, Slug, Product

# Register your models here.
admin.site.register(Recipient)
admin.site.register(Slug)
admin.site.register(Product)
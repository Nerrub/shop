# flower_shop/cart/admin.py
from django.contrib import admin
from .models import Product
from .models import Flower

admin.site.register(Product)

class FlowerAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at']
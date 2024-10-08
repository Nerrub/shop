# flower_shop/cart/admin.py
from django.contrib import admin
from .models import Product
from .models import Flower

admin.site.register(Product)

class FlowerAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'updated_at')  # Отображаемые поля в списке товаров
    list_filter = ('price', 'created_at')  # Возможность фильтрации по цене и дате создания
    search_fields = ('name',)  # Поиск по имени продукта
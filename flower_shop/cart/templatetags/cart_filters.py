# flower_shop/cart/templatetags/cart_filters.py

from django import template

register = template.Library()

@register.filter
def get_total_price(cart):
    return sum(item['price'] * item['quantity'] for item in cart)

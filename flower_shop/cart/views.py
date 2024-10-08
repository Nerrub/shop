# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from .models import Product

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def flower_catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'cart/flower_catalog.html', {'flowers': flowers})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Получаем продукт по ID или возвращаем 404, если не найден
    return render(request, 'cart/product_detail.html', {'product': product})
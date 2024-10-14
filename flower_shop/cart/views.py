# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from .models import Product
from .forms import OrderForm
from .models import Order
from .models import Product, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from bot.telegram_bot import send_order_notification
import asyncio

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)  # Добавляем товар с количеством 1
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    total_price = cart.get_total_price()  # Получаем общую стоимость корзины
    return render(request, 'cart/detail.html', {'cart': cart, 'total_price': total_price})


def flower_catalog(request):
    flowers = Product.objects.all()
    return render(request, 'cart/flower_catalog.html', {'flowers': flowers})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Получаем продукт по ID или возвращаем 404, если не найден
    return render(request, 'cart/product_detail.html', {'product': product})

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def checkout_view(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
                user=request.user
            )
            order.save()

            # Отправка уведомления в телеграм-бот
            order_info = {
                'name': order.name,
                'address': order.address,
                'phone': order.phone,
                'total_price': order.total_price,
            }
            asyncio.run(send_order_notification(order_info))

            # Очистка корзины
            cart.clear()

            return redirect('cart:order_success')
    else:
        form = OrderForm()

    return render(request, 'cart/checkout.html', {'form': form, 'cart': cart})

def order_success_view(request):
    return render(request, 'cart/order_success.html')

def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'cart/order_history.html', {'orders': orders})

def reorder_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # Логика для повторного добавления продуктов из заказа в корзину

    return redirect('cart:checkout')

def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('cart:product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'cart/add_review.html', {'form': form, 'product': product})
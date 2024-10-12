from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from .models import Product
from cart.models import Order
from django.shortcuts import get_object_or_404

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Аутентификация пользователя после регистрации
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Переход на главную страницу
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Переход на главную страницу
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')  # Указываем полное имя URL с пространством имен
    return render(request, 'accounts/logout.html')


def profile_view(request):
    # Получаем заказы, принадлежащие текущему пользователю
    orders = Order.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'orders': orders})

def reorder_view(request, order_id):
    # Получаем заказ, который нужно повторить
    original_order = get_object_or_404(Order, id=order_id, user=request.user)

    # Создаем новый заказ на основе оригинального
    new_order = Order.objects.create(
        user=request.user,
        name=original_order.name,
        address=original_order.address,
        phone=original_order.phone,
        status='accepted',  # Устанавливаем статус как 'accepted'
    )

    # Копируем элементы из оригинального заказа в новый заказ
    for item in original_order.items.all():
        new_item = OrderItem.objects.create(
            order=new_order,
            product=item.product,
            quantity=item.quantity,
            price=item.price,
        )
        new_item.save()

    # Перенаправляем пользователя на страницу истории заказов
    return redirect('accounts:profile')
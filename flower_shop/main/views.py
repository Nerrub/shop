from django.shortcuts import render
from cart.models import Product
def home_view(request):
    # Получаем все продукты из базы данных
    products = Product.objects.all()
    # Передаем продукты в шаблон
    return render(request, 'flower_shop/home.html', {'products': products})
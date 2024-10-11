from django.shortcuts import render
from cart.models import Product
from analytics.views import create_report_view
def home_view(request):
    # Получаем все продукты из базы данных
    products = Product.objects.all()
    # Передаем продукты в шаблон
    return render(request, 'flower_shop/home.html', {'products': products})
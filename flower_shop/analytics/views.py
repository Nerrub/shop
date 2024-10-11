# flower_shop/analytics/views.py

from django.shortcuts import render
from cart.models import Order
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def generate_report(request):
    # Получение всех заказов
    orders = Order.objects.all()

    # Расчет количества заказов и общего дохода за текущий день
    today_orders = orders.filter(created_at__date=datetime.date.today())
    total_revenue_today = sum(order.get_total_price() for order in today_orders)

    context = {
        'orders': orders,
        'today_orders_count': today_orders.count(),
        'total_revenue_today': total_revenue_today,
    }

    # Рендеринг отчета в шаблон и сохранение как файл analytics.html
    response = render(request, 'analytics/analytics.html', context)
    with open('analytics.html', 'w', encoding='utf-8') as file:
        file.write(response.content.decode('utf-8'))

    return response


def create_report_view(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    total_revenue = sum(order.get_total_price() for order in orders)

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
    }

    # Сохранение отчета в HTML-файл
    return render(request, 'analytics/analytics.html', context)
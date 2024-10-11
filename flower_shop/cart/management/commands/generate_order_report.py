from django.core.management.base import BaseCommand
from cart.models import Order
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate a daily report of orders'

    def handle(self, *args, **kwargs):
        # Определяем дату начала и конца сегодняшнего дня
        start_of_day = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        # Получаем заказы за сегодняшний день
        orders_today = Order.objects.filter(created_at__gte=start_of_day, created_at__lt=end_of_day)

        # Подсчитываем количество и общую сумму
        total_orders = orders_today.count()
        total_revenue = sum(order.get_total_price() for order in orders_today)  # Предполагается, что у вас есть метод get_total_price

        # Составляем информацию для отчета
        report_lines = [
            f"Дата: {timezone.now().date()}",
            f"Количество заказов: {total_orders}",
            f"Общая сумма заработка: ${total_revenue}",
            "Заказы за сегодня:"
        ]

        for order in orders_today:
            report_lines.append(f"Заказ #{order.id}: Статус - {order.get_status_display()}, Сумма - ${order.get_total_price()}")

        # Записываем отчет в файл
        report_file_path = 'order_report.txt'
        with open(report_file_path, 'a', encoding='utf-8') as report_file:
            report_file.write("\n".join(report_lines) + "\n\n")

        self.stdout.write(self.style.SUCCESS('Отчет успешно создан'))

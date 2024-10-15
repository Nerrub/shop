from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class Flower(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='flowers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='accepted',
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Проверяем, изменился ли статус
        if self.pk:
            previous = Order.objects.get(pk=self.pk)
            if previous.status != self.status:
                # Отправляем уведомление в телеграм бот
                send_order_notification(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"
    def __str__(self):
        return f"Order #{self.id} - {self.status}"

    def calculate_total_price(self):
        """
        Метод для расчета общей стоимости заказа на основе связанных элементов.
        """
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_price = total
        self.save()

    @classmethod
    def save_order_data_to_file(cls):
        """
        Метод для записи аналитики по заказам в текстовый файл.
        """
        import os
        from datetime import date

        # Определяем путь к файлу для записи аналитики
        file_path = os.path.join('analytics', 'order_analytics.txt')

        # Подсчитываем заказы и общую выручку за сегодняшний день
        today = date.today()
        orders_today = cls.objects.filter(created_at__date=today)
        total_revenue_today = sum(order.total_price for order in orders_today)
        total_orders_today = orders_today.count()

        # Форматируем данные для записи
        data = [
            f"Дата: {today}\n",
            f"Количество заказов за день: {total_orders_today}\n",
            f"Общая выручка за день: {total_revenue_today}\n",
            f"Список заказов:\n"
        ]
        for order in orders_today:
            data.append(
                f"Заказ #{order.id}: Статус - {order.get_status_display()}, Сумма - {order.total_price}\n"
            )
        data.append("\n" + "="*50 + "\n")

        # Проверяем, существует ли директория и файл, и создаем их, если необходимо
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Записываем данные в файл
        with open(file_path, 'a', encoding='utf-8') as file:
            file.writelines(data)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        """
        Метод для получения общей стоимости элемента заказа.
        """
        return self.quantity * self.price

    def __str__(self):
        return f"Item {self.product.name} (x{self.quantity})"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"

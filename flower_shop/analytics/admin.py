from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import path
from django.http import HttpResponse
from cart.models import Order
from .views import create_report_view


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'updated_at')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create-report/', self.admin_site.admin_view(self.create_report), name='create-report'),
        ]
        return custom_urls + urls

    def create_report(self, request):
        # Используем представление для создания отчета
        response = create_report_view(request)
        return response

    def create_report_link(self, obj):
        return format_html(
            '<a class="button" href="{}">Создать отчет</a>',
            reverse('admin:create-report')
        )

    create_report_link.short_description = 'Создать отчет'
    create_report_link.allow_tags = True

    # Добавляем кнопку в админку
    change_list_template = "admin/order_changelist.html"

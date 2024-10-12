# analytics/urls.py
from django.urls import path
from .views import create_report_view

app_name = 'analytics'  # Обратите внимание, что пространство имен установлено

urlpatterns = [
    path('generate_report/', create_report_view, name='generate_report'),
]
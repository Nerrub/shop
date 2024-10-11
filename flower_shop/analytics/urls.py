# analytics/urls.py
from django.urls import path
from .views import create_report_view

app_name = 'analytics'

urlpatterns = [
    path('create-report/', create_report_view, name='create_report'),
]

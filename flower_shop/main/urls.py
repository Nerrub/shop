from django.urls import path
from . import views

app_name = 'main'  # Задаем пространство имен для приложения

urlpatterns = [
    path('', views.home_view, name='home'),

]
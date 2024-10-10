# flower_shop/urls.py
from django.contrib import admin  # Импортируем admin
from django.urls import path, include
from main.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', home_view, name='home'),
    path('', include('main.urls', namespace='main')),
]

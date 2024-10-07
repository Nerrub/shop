# flower_shop/urls.py
from django.contrib import admin  # Импортируем admin
from django.urls import path, include
from accounts.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', home_view, name='home'),
]

# cart/urls.py
from django.urls import path
from . import views
from .views import order_history_view

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('catalog/', views.flower_catalog, name='catalog'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove/<int:product_id>/', views.cart_remove, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/', views.order_success_view, name='order_success'),
    path('order-history/', order_history_view, name='order_history'),
    path('reorder/<int:order_id>/', views.reorder_view, name='reorder'),
]



    # Другие URL

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='orders-create'),
    path('<int:order_id>/pay/', views.pay_order, name='orders-pay'),
    path('fish-sales-order/', views.fish_sales_order, name='fish-sales-order'),
    path('list/', views.list_products, name='products-list'),
]

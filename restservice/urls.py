from django.contrib import admin
from django.urls import path

from rest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('couriers', views.couriers, name="couriers"),
    path('couriers/<int:courier_id>', views.patch_couriers, name="patch_couriers"),
    path('orders', views.orders, name="orders"),
    path('orders/assign', views.orders_assign, name="orders_assign"),
    path('orders/complete', views.orders_complete, name="orders_complete")
]

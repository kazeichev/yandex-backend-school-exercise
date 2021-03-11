from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from rest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url('couriers', views.couriers, name="couriers")
]

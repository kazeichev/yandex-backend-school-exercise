from django.contrib import admin

from rest import models

admin.site.register(models.Courier)
admin.site.register(models.Order)
admin.site.register(models.CourierOrder)
admin.site.register(models.CourierWorkingHour)
admin.site.register(models.OrderDeliveryHour)

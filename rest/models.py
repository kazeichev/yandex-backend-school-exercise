from django.db import models
from django.db.models import Sum


class Courier(models.Model):
    TYPE_FOOT = 'foot'
    TYPE_BIKE = 'bike'
    TYPE_CAR = 'car'

    TYPES_WEIGHT = [
        (TYPE_FOOT, 10),
        (TYPE_BIKE, 15),
        (TYPE_CAR, 50),
    ]

    courier_id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)
    courier_type = models.CharField(choices=TYPES_WEIGHT, null=False, blank=False, max_length=10)
    regions = models.JSONField(null=False, blank=False)

    def is_foot_type(self):
        return self.courier_type == self.TYPE_FOOT

    def is_bike_type(self):
        return self.courier_type == self.TYPE_BIKE

    def is_car_type(self):
        return self.courier_type == self.TYPE_BIKE

    def get_max_weight(self):
        return dict(self.TYPES_WEIGHT)[str(self.courier_type)]

    def get_working_hours(self):
        hours = []
        for item in CourierWorkingHour.objects.filter(courier=self).all():
            hours.append("{}-{}".format(item.start_time.strftime("%H:%M"), item.end_time.strftime("%H:%M")))

        return hours

    def get_free_weight(self):
        assigned_orders_weight = CourierOrder.objects\
            .filter(courier=self, complete_time__isnull=True)\
            .values('order__weight')\
            .aggregate(Sum('order__weight'))['order__weight__sum']

        return max(0, self.get_max_weight() - (0 if assigned_orders_weight is None else assigned_orders_weight))


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)
    weight = models.FloatField(null=False, blank=False)
    region = models.IntegerField(null=False, blank=False)


class CourierWorkingHour(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)


class OrderDeliveryHour(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)


class CourierOrder(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    assign_time = models.DateTimeField(blank=False, null=False)
    complete_time = models.DateTimeField(blank=True, null=True)

from django.db import models


class Courier(models.Model):
    TYPE_FOOT = 'foot'
    TYPE_BIKE = 'bike'
    TYPE_CAR = 'car'

    TYPES_WEIGHT = [
        (TYPE_FOOT, 10),
        (TYPE_BIKE, 15),
        (TYPE_CAR, 50),
    ]

    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)
    type = models.CharField(choices=TYPES_WEIGHT, null=False, blank=False, max_length=10)
    regions = models.JSONField(null=False, blank=False)
    working_hours = models.DurationField(null=False, blank=False)

    def is_foot_type(self):
        return self.type == self.TYPE_FOOT

    def is_bike_type(self):
        return self.type == self.TYPE_BIKE

    def is_car_type(self):
        return self.type == self.TYPE_BIKE


class Order(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)
    weight = models.FloatField(null=False, blank=False)
    region = models.IntegerField(null=False, blank=False)
    delivery_hours = models.DurationField(null=False, blank=False)


class CourierOrder(models.Model):
    STATUS_CREATED = 100
    STATUS_COMPLETED = 200

    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.SmallIntegerField(null=False, blank=False, default=STATUS_CREATED)

    def is_created(self):
        return self.status == self.STATUS_CREATED

    def is_completed(self):
        return self.status == self.STATUS_COMPLETED

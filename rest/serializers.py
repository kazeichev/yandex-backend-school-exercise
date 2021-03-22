from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from rest.managers import OrderManager, CourierManager
from rest.models import Courier, CourierWorkingHour, Order


class CourierSerializer(serializers.ModelSerializer):
    courier_id = serializers.IntegerField(
        required=True,
        allow_null=False,
        validators=[UniqueValidator(queryset=Courier.objects.all())]
    )
    working_hours = serializers.JSONField(required=True, allow_null=False)

    class Meta:
        model = Courier
        fields = ('courier_id', 'courier_type', 'regions', 'working_hours')

    def validate(self, data):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                raise ValidationError("Got unknown fields: {}".format(unknown_keys))

        return data

    def create(self, validated_data):
        courier = CourierManager.create(
            validated_data.get('courier_id'),
            validated_data.get('courier_type'),
            validated_data.get('regions'),
            validated_data.get('working_hours')
        )

        return courier

    def update(self, instance, validated_data):
        if next(iter(validated_data)) == "working_hours":
            working_hours = CourierWorkingHour.objects.filter(courier=instance)
            working_hours.delete()

            for data in next(iter(validated_data.values())):
                hours = data.split("-")
                CourierWorkingHour.objects.create(
                    courier=instance,
                    start_time=hours[0],
                    end_time=hours[1]
                )

        instance.courier_type = validated_data.get("courier_type", instance.courier_type)
        instance.regions = validated_data.get("regions", instance.regions)
        instance.save()

        return instance


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(
        required=True,
        allow_null=False,
        validators=[UniqueValidator(queryset=Order.objects.all())]
    )
    delivery_hours = serializers.JSONField(required=True, allow_null=False)

    class Meta:
        model = Order
        fields = ('order_id', 'weight', 'region', 'delivery_hours')

    def validate(self, data):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                raise ValidationError("Got unknown fields: {}".format(unknown_keys))

        return data

    def create(self, validated_data):
        order = OrderManager.create(
            validated_data.get('order_id'),
            validated_data.get('weight'),
            validated_data.get('region'),
            validated_data.get('delivery_hours')
        )

        return order

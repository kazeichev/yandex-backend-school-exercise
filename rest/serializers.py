from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from rest.models import Courier, CourierWorkingHour


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
        courier = Courier.objects.create(
            courier_id=validated_data.get('courier_id'),
            courier_type=validated_data.get('courier_type'),
            regions=validated_data.get('regions')
        )

        for time in validated_data.get('working_hours'):
            hours = time.split("-")
            CourierWorkingHour.objects.create(
                courier=courier,
                start_time=hours[0],
                end_time=hours[1]
            )

        return courier

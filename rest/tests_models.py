import datetime

from django.test import TestCase
from rest.models import Courier, Order, CourierOrder, CourierWorkingHour, OrderDeliveryHour


class CreateCourierTestCase(TestCase):
    """ Создание сущности Курьер """

    def setUp(self) -> None:
        courier = Courier.objects.create(
            id=3,
            type=Courier.TYPE_BIKE,
            regions=[1, 2, 3]
        )

        CourierWorkingHour.objects.create(
            courier=courier,
            start_time="09:00",
            end_time="18:00"
        )

    def test(self):
        courier = Courier.objects.get(id=3)
        workingHours = CourierWorkingHour.objects.get(courier=courier)

        TestCase.assertTrue(self, Courier.objects.filter(id=3).exists())
        TestCase.assertTrue(self, CourierWorkingHour.objects.filter(courier=courier).exists())

        TestCase.assertEquals(self, [1, 2, 3], courier.regions)
        TestCase.assertIn(self, 3, courier.regions)

        TestCase.assertTrue(self, courier.is_bike_type())

        TestCase.assertEqual(self, datetime.time(9, 0), workingHours.start_time)
        TestCase.assertEqual(self, datetime.time(18, 0), workingHours.end_time)


class CreateOrderTestCase(TestCase):
    """ Создание сущности Заказ """

    def setUp(self) -> None:
        order = Order.objects.create(
            id=5,
            weight=3.7,
            region=3
        )

        OrderDeliveryHour.objects.create(
            order=order,
            start_time="09:00",
            end_time="18:00"
        )

    def test(self):
        order = Order.objects.get(id=5)
        deliveryHours = OrderDeliveryHour.objects.get(order=order)

        TestCase.assertTrue(self, Order.objects.filter(id=5).exists())
        TestCase.assertTrue(self, OrderDeliveryHour.objects.filter(order=order).exists())

        TestCase.assertTrue(self, order.weight == 3.7)
        TestCase.assertTrue(self, order.region == 3)

        TestCase.assertEqual(self, datetime.time(9, 0), deliveryHours.start_time)
        TestCase.assertEqual(self, datetime.time(18, 0), deliveryHours.end_time)

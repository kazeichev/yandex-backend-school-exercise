import datetime

from django.test import TestCase
from rest.models import Courier, Order, CourierOrder, CourierWorkingHour, OrderDeliveryHour


class CreateCourierTestCase(TestCase):
    """ Создание сущности Курьер """

    def setUp(self) -> None:
        courier = Courier.objects.create(
            courier_id=3,
            courier_type=Courier.TYPE_BIKE,
            regions=[1, 2, 3]
        )

        CourierWorkingHour.objects.create(
            courier=courier,
            start_time="09:00",
            end_time="18:00"
        )

    def test(self):
        courier = Courier.objects.get(courier_id=3)
        workingHours = CourierWorkingHour.objects.get(courier=courier)

        self.assertTrue(Courier.objects.filter(courier_id=3).exists())
        self.assertTrue(CourierWorkingHour.objects.filter(courier=courier).exists())

        self.assertEquals([1, 2, 3], courier.regions)
        self.assertIn(3, courier.regions)

        self.assertTrue(courier.is_bike_type())

        self.assertEqual(datetime.time(9, 0), workingHours.start_time)
        self.assertEqual(datetime.time(18, 0), workingHours.end_time)


class CreateOrderTestCase(TestCase):
    """ Создание сущности Заказ """

    def setUp(self) -> None:
        order = Order.objects.create(
            order_id=5,
            weight=3.7,
            region=3
        )

        OrderDeliveryHour.objects.create(
            order=order,
            start_time="09:00",
            end_time="18:00"
        )

    def test(self):
        order = Order.objects.get(order_id=5)
        deliveryHours = OrderDeliveryHour.objects.get(order=order)

        self.assertTrue(Order.objects.filter(order_id=5).exists())
        self.assertTrue(OrderDeliveryHour.objects.filter(order=order).exists())

        self.assertTrue(order.weight == 3.7)
        self.assertTrue(order.region == 3)

        self.assertEqual(datetime.time(9, 0), deliveryHours.start_time)
        self.assertEqual(datetime.time(18, 0), deliveryHours.end_time)


class CreateCourierOrderTestCase(TestCase):
    """ Создание сущности Заказ Курьера """

    def setUp(self) -> None:
        courier = Courier.objects.create(
            courier_id=3,
            courier_type=Courier.TYPE_BIKE,
            regions=[1, 2, 3]
        )

        order = Order.objects.create(
            order_id=5,
            weight=3.7,
            region=3
        )

        CourierOrder.objects.create(
            courier=courier,
            order=order
        )

    def test(self):
        courier = Courier.objects.get(courier_id=3)
        order = Order.objects.get(order_id=5)

        self.assertTrue(Courier.objects.filter(courier_id=3).exists())
        self.assertTrue(Order.objects.filter(order_id=5).exists())
        self.assertTrue(CourierOrder.objects.filter(order=order, courier=courier).exists())

import datetime

from django.test import TestCase

from rest.managers import CourierOrderManager, CourierManager, OrderManager
from rest.models import Courier, Order, CourierOrder, CourierWorkingHour, OrderDeliveryHour


class CreateCourierTestCase(TestCase):
    """ Создание сущности Курьер """

    def setUp(self) -> None:
        CourierManager.create(3, Courier.TYPE_BIKE, [1, 2, 3], ["09:00-18:00"])

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
        OrderManager.create(5, 3.7, 3, ["09:00-18:00"])

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
        courier = CourierManager.create(3, Courier.TYPE_BIKE, [1, 2, 3], ["09:00-18:00"])
        order = OrderManager.create(5, 3.7, 3, ["09:00-12:00"])

        CourierOrderManager.create(courier, order)

    def test(self):
        courier = Courier.objects.get(courier_id=3)
        order = Order.objects.get(order_id=5)

        self.assertTrue(Courier.objects.filter(courier_id=3).exists())
        self.assertTrue(Order.objects.filter(order_id=5).exists())
        self.assertTrue(CourierOrder.objects.filter(order=order, courier=courier).exists())

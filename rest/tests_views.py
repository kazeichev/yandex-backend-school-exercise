import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from rest.managers import OrderManager, CourierManager, CourierOrderManager
from rest.models import Courier, CourierWorkingHour

client = APIClient()


class CreateCourierTestCase(TestCase):
    """ Тестируем добавление курьеров """

    def setUp(self) -> None:
        self.valid_data = {
            "data": [
                {
                    "courier_id": 1,
                    "courier_type": Courier.TYPE_FOOT,
                    "regions": [1, 22, 30],
                    "working_hours": ["09:00-14:00", "15:00-20:00"]
                },
                {
                    "courier_id": 2,
                    "courier_type": Courier.TYPE_BIKE,
                    "regions": [13],
                    "working_hours": ["09:00-14:00"]
                }
            ]
        }

        self.invalid_data = {
            "data": [
                {
                    "courier_id": 1,
                    "courier_type": Courier.TYPE_FOOT,
                    "regions": [1, 22, 30],
                    "working_hours": ["09:00-14:00", "15:00-20:00"]
                },
                {
                    "courier_id": 3,
                    "courier_type": Courier.TYPE_BIKE,
                    "regions": [13],
                    "working_hours": ["09:00-14:00"]
                }
            ]
        }

        self.extra_field = {
            "data": [
                {
                    "courier_id": 4,
                    "courier_type": Courier.TYPE_FOOT,
                    "regions": [1, 22, 30],
                    "working_hours": ["09:00-14:00", "15:00-20:00"],
                    "rating": 5
                }
            ]
        }

    def test_valid_data(self):
        response = client.post(reverse("couriers"), self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"couriers": [{"id": 1}, {"id": 2}]})

    def test_invalid_data(self):
        CourierManager.create(1, Courier.TYPE_FOOT, [1, 22, 30], ["09:00-12:00"])

        response = client.post(reverse("couriers"), self.invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"validation_error": {
            "couriers": [{"id": 1}]
        }})

    def test_extra_field(self):
        response = client.post(reverse("couriers"), self.extra_field, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"validation_error": {
            "couriers": [{"id": 4}]
        }})


class PatchCourierTestCase(TestCase):
    """ Тестируем обновление курьера по его ID """

    def setUp(self) -> None:
        self.courier = CourierManager.create(1, Courier.TYPE_FOOT, [1, 22, 30], ["09:00-12:00"])

        self.test_valid_data_1 = {
            "courier_type": Courier.TYPE_BIKE
        }

        self.test_valid_data_2 = {
            "regions": [15]
        }

        self.test_valid_data_3 = {
            "working_hours": ["08:00-16:00", "18:00-21:00"]
        }

    def test_change_courier_type(self):
        response = client.patch(reverse("patch_couriers", args=(1,)), self.test_valid_data_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "courier_id": 1,
            "courier_type": Courier.TYPE_BIKE,
            "regions": [1, 22, 30],
            "working_hours": ["09:00-12:00"]
        })

    def test_change_courier_regions(self):
        response = client.patch(reverse("patch_couriers", args=(1,)), self.test_valid_data_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "courier_id": 1,
            "courier_type": Courier.TYPE_FOOT,
            "regions": [15],
            "working_hours": ["09:00-12:00"]
        })

    def test_change_courier_working_hours(self):
        response = client.patch(reverse("patch_couriers", args=(1,)), self.test_valid_data_3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "courier_id": 1,
            "courier_type": Courier.TYPE_FOOT,
            "regions": [1, 22, 30],
            "working_hours": ["08:00-16:00", "18:00-21:00"]
        })

        self.assertTrue(len(CourierWorkingHour.objects.filter(courier=self.courier).all()) == 2)

    def test_clean_working_hours(self):
        response = client.patch(reverse("patch_couriers", args=(1,)), {"working_hours": []})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "courier_id": 1,
            "courier_type": Courier.TYPE_FOOT,
            "regions": [1, 22, 30],
            "working_hours": []
        })

        self.assertFalse(CourierWorkingHour.objects.filter(courier=self.courier).exists())


class CreateOrderTestCase(TestCase):
    """ Тестируем добавление заказов """

    def setUp(self) -> None:
        self.valid_data = {
            "data": [
                {
                    "order_id": 1,
                    "weight": 0.23,
                    "region": 12,
                    "delivery_hours": ["09:00-12:00"]
                },
                {
                    "order_id": 2,
                    "weight": 1.68,
                    "region": 32,
                    "delivery_hours": ["12:00-18:00", "20:00-00:00"]
                }
            ]
        }

        self.extra_fields = {
            "data": [
                {
                    "order_id": 1,
                    "weight": 0.23,
                    "region": 12,
                    "delivery_hours": ["09:00-12:00"],
                    "rating": 5
                }
            ]
        }

    def test_valid_data(self):
        response = client.post(reverse("orders"), self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            "orders": [{"id": 1}, {"id": 2}]
        })

    def test_extra_fields(self):
        response = client.post(reverse("orders"), self.extra_fields)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            "validation_error": {
                "orders": [{"id": 1}]
            }
        })


class AssignOrdersTestCase(TestCase):
    """ Тестируем назначение заказов курьерам """

    def setUp(self) -> None:
        self.assign_time = datetime.datetime.now()

        self.order_1 = OrderManager.create(1, 4, 1, ["09:00-12:00", "15:00-20:00"])
        self.order_2 = OrderManager.create(2, 2.5, 22, ["09:00-22:00"])
        self.order_3 = OrderManager.create(3, 3.5, 30, ["09:00-12:00"])
        self.order_4 = OrderManager.create(4, 2, 1, ["09:00-12:00"])
        self.order_5 = OrderManager.create(5, 8, 2, ["09:00-15:00"])

        self.courier = CourierManager.create(1, Courier.TYPE_FOOT, [1, 22, 30], ["09:00-12:00", "14:00-20:00"])

    def test_without_assigned_orders(self):
        response = client.post(reverse("orders_assign"), {"courier_id": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['orders'], [{"id": 1}, {"id": 3}, {"id": 2}])

    def test_with_assigned_orders(self):
        order_time = datetime.datetime.now()
        CourierOrderManager.create(self.courier, self.order_1, order_time)
        response = client.post(reverse("orders_assign"), {"courier_id": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['orders'], [{"id": 3}, {"id": 2}])
        self.assertEqual(response.data['assign_time'], order_time.isoformat())

    def test_with_completed_orders(self):
        first_order_time = datetime.datetime.now().isoformat()
        CourierOrderManager.create(self.courier, self.order_2, first_order_time,
                                   datetime.datetime.now() + datetime.timedelta(hours=1))

        response = client.post(reverse("orders_assign"), {"courier_id": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['orders'], [{"id": 1}, {"id": 3}, {"id": 4}])
        self.assertNotEqual(response.data['assign_time'], first_order_time)

    def test_without_free_weight(self):
        CourierOrderManager.create(self.courier, self.order_1, datetime.datetime.now())
        CourierOrderManager.create(self.courier, self.order_2, datetime.datetime.now())
        CourierOrderManager.create(self.courier, self.order_3, datetime.datetime.now())

        response = client.post(reverse("orders_assign"), {"courier_id": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"orders": []})

    def test_assign_to_several_couriers(self):
        self.courier_2 = CourierManager.create(2, Courier.TYPE_BIKE, [22, 50], ["09:00-14:00"])
        CourierOrderManager.create(self.courier_2, self.order_2)

        response = client.post(reverse("orders_assign"), {"courier_id": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['orders'], [{"id": 1}, {"id": 3}, {"id": 4}])

    def test_incorrect_courier_id(self):
        response = client.post(reverse("orders_assign"), {"courier_id": 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CompleteOrderTestCase(TestCase):
    """ Тестируем завершение заказа """

    def setUp(self) -> None:
        self.assign_time = datetime.datetime.now()
        self.order = OrderManager.create(1, 4, 1, ["09:00-12:00", "15:00-20:00"])
        self.courier = CourierManager.create(1, Courier.TYPE_FOOT, [1, 22, 30], ["09:00-12:00", "14:00-20:00"])
        self.courier_order = CourierOrderManager.create(self.courier, self.order, self.assign_time)

    def test_successfully_complete_order(self):
        response = client.post(reverse("orders_complete"), {
            "courier_id": 1,
            "order_id": 1,
            "complete_time": datetime.datetime.now() + datetime.timedelta(hours=1)
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"order_id": 1})

    def test_incorrect_data(self):
        response = client.post(reverse("orders_complete"), {
            "courier_id": 2,
            "order_id": 1,
            "complete_time": datetime.datetime.now() + datetime.timedelta(hours=1)
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data)

        response = client.post(reverse("orders_complete"), {
            "courier_id": 1,
            "order_id": 2,
            "complete_time": datetime.datetime.now() + datetime.timedelta(hours=1)
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data)

        response = client.post(reverse("orders_complete"), {
            "courier_id": 3,
            "order_id": 3,
            "complete_time": datetime.datetime.now() + datetime.timedelta(hours=1)
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data)

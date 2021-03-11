from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from rest.models import Courier, CourierWorkingHour

client = APIClient()


class CreateCourierTestCase(TestCase):
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
        Courier.objects.create(
            courier_id=1,
            courier_type=Courier.TYPE_FOOT,
            regions=[1, 22, 30]
        )

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
    def setUp(self) -> None:
        self.courier = Courier.objects.create(
            courier_id=1,
            courier_type=Courier.TYPE_FOOT,
            regions=[1, 22, 30]
        )

        CourierWorkingHour.objects.create(
            courier=self.courier,
            start_time="09:00",
            end_time="12:00"
        )

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

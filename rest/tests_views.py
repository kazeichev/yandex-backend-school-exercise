from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from rest.models import Courier

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

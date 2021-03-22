from django.db import DatabaseError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest.managers import OrderManager
from rest.models import Courier
from rest.serializers import CourierSerializer, OrderSerializer


@api_view(['POST'])
def couriers(request):
    try:
        not_valid_couriers = []
        valid_couriers = []

        for data in request.data['data']:
            serializer = CourierSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                valid_couriers.append({"id": serializer.validated_data["courier_id"]})
            else:
                not_valid_couriers.append({"id": data["courier_id"]})

        if len(not_valid_couriers) > 0:
            return Response({
                "validation_error": {
                    "couriers": not_valid_couriers
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"couriers": valid_couriers}, status=status.HTTP_201_CREATED)

    except RuntimeError:
        return Response(status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def patch_couriers(request, courier_id):  # TODO перераспределение заказов, если изменен тип, часы, регионы
    courier = Courier.objects.get(courier_id=courier_id)
    serializer = CourierSerializer(courier, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "courier_id": courier.courier_id,
            "courier_type": courier.courier_type,
            "regions": courier.regions,
            "working_hours": courier.get_working_hours()
        }, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def orders(request):
    try:
        not_valid_orders = []
        valid_orders = []

        for data in request.data['data']:
            serializer = OrderSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                valid_orders.append({"id": serializer.validated_data["order_id"]})
            else:
                not_valid_orders.append({"id": data["order_id"]})

        if len(not_valid_orders) > 0:
            return Response({
                "validation_error": {
                    "orders": not_valid_orders
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"orders": valid_orders}, status=status.HTTP_201_CREATED)

    except RuntimeError:
        return Response(status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def orders_assign(request):
    try:
        couriers_id = request.data['courier_id']
        orders_to_assign = OrderManager.get_orders_to_assign(couriers_id)

        return Response(OrderManager.assign_orders_to_courier(couriers_id, orders_to_assign), status=status.HTTP_200_OK)
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def orders_complete(request):
    try:
        courier_id = request.data['courier_id']
        order_id = request.data['order_id']
        complete_time = request.data['complete_time']

        return Response(OrderManager.complete(courier_id, order_id, complete_time), status=status.HTTP_200_OK)
    except DatabaseError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest.serializers import CourierSerializer


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

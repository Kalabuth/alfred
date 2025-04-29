from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.addresses.models.address import Address
from apps.authentication.mixins.api_key_protected_view_mixin import (
    ApiKeyProtectedViewMixin,
)
from apps.common.methods.custom_pagination import CustomPagination
from apps.drivers.models.driver import Driver
from apps.drivers.serializers.driver_serializer import DriverSerializer
from apps.services.methods.calculate_distance import calculate_distance
from apps.services.methods.estimate_arrival_time import estimate_arrival_time


class DriverView(ApiKeyProtectedViewMixin, viewsets.GenericViewSet):
    """
    list:
      GET /drivers/
      List all drivers.

    create:
      POST /drivers/
      Create a new driver.

    retrieve:
      GET /drivers/{id}/
      Retrieve a driver by its id.

    update_availability:
      POST /drivers/{id}/update_availability/
      Mark a driver as available or unavailable.
    """

    queryset = Driver.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        return DriverSerializer

    @swagger_auto_schema(
        operation_summary="List Drivers",
        operation_description="Returns a list of all drivers in the system.",
        responses={200: DriverSerializer(many=True)},
    )
    def list(self, request):
        drivers = self.get_queryset()
        page = self.paginate_queryset(drivers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(drivers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Retrieve Driver",
        responses={200: DriverSerializer, 404: "Not Found"},
    )
    def retrieve(self, request, pk=None):
        driver = self.get_object()
        serializer = self.get_serializer(driver)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update Driver Availability",
        operation_description="Update the availability status of a driver.",
        responses={200: DriverSerializer, 400: "Bad Request"},
    )
    @action(detail=True, methods=["post"])
    def update_availability(self, request, pk=None):
        driver = self.get_object()
        driver.is_available = request.data.get("is_available", driver.is_available)
        driver.save(update_fields=["is_available"])
        return Response({"status": "success", "is_available": driver.is_available})

    @swagger_auto_schema(
        operation_summary="List Closest Drivers",
        operation_description="List drivers ordered by distance to a given address (address_id).",
        responses={200: "List of drivers ordered by distance", 404: "Address Not Found"},
    )
    @action(
        detail=False, methods=["get"], url_path="closest-drivers/(?P<address_id>[^/.]+)"
    )
    def closest_drivers(self, request, address_id=None):
        try:
            client_address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return Response(
                {"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND
            )

        client_lat = client_address.latitude
        client_lng = client_address.longitude

        available_drivers = Driver.objects.filter(is_available=True).select_related(
            "current_location"
        )

        drivers_with_distance = []
        for driver in available_drivers:
            if not driver.current_location:
                continue
            driver_lat = driver.current_location.latitude
            driver_lng = driver.current_location.longitude
            distance = calculate_distance(driver_lat, driver_lng, client_lat, client_lng)
            arrival_time_min = estimate_arrival_time(distance)
            drivers_with_distance.append(
                {
                    "driver_id": driver.id,
                    "driver_name": f"{driver.user.full_name}",
                    "distance_km": round(distance, 2),
                    "estimated_arrival_time_min": arrival_time_min,
                    "address_id": driver.current_location.id,
                }
            )

        drivers_with_distance.sort(key=lambda x: x["distance_km"])

        return Response(drivers_with_distance, status=status.HTTP_200_OK)

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from apps.authentication.mixins.api_key_protected_view_mixin import (
    ApiKeyProtectedViewMixin,
)
from apps.common.methods.custom_pagination import CustomPagination
from apps.services.choices.status_service import ServiceStatus
from apps.services.models.service import Service
from apps.services.serializers.service_serializer import (
    ServiceCreateSerializer,
    ServiceSerializer,
)
from apps.services.services.assign_driver import assign_driver_to_service


class ServiceView(ApiKeyProtectedViewMixin, viewsets.GenericViewSet):
    """
    list:
      GET /services/
      List all services.

    create:
      POST /services/
      Create a new service request.

    retrieve:
      GET /services/{id}/
      Retrieve a service by its id.

    complete:
      POST /services/{id}/complete/
      Mark a service as completed.
    """

    queryset = Service.objects.select_related("client_address", "driver").all()
    parser_classes = [JSONParser]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "create":
            return ServiceCreateSerializer
        return ServiceSerializer

    @swagger_auto_schema(
        operation_summary="List Services",
        responses={200: ServiceSerializer(many=True), 403: "Forbidden"},
    )
    def list(self, request):
        service = self.get_queryset()
        page = self.paginate_queryset(service)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(service, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create Service",
        request_body=ServiceCreateSerializer,
        responses={201: ServiceSerializer, 400: "Bad Request", 403: "Forbidden"},
    )
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = serializer.save()
        assign_driver_to_service(service)
        output = ServiceSerializer(service)
        return Response(output.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Retrieve Service",
        responses={200: ServiceSerializer, 404: "Not Found", 403: "Forbidden"},
    )
    def retrieve(self, request, pk=None):
        service = self.get_object()
        serializer = self.get_serializer(service)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Complete Service",
        operation_description="Mark a service as completed if assigned.",
        responses={
            200: ServiceSerializer,
            400: "If the service is not in ASSIGNED status",
            403: "Forbidden",
        },
    )
    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        service = self.get_object()
        if service.status != ServiceStatus.IN_PROGRESS:
            return Response(
                {"detail": "Only assigned services can be completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        service.status = ServiceStatus.COMPLETED
        service.save()
        serializer = self.get_serializer(service)
        return Response(serializer.data)

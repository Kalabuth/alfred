from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.addresses.models.address import Address
from apps.addresses.serializers.address_serializer import (
    AddressCreateSerializer,
    AddressSerializer,
)
from apps.authentication.mixins.api_key_protected_view_mixin import (
    ApiKeyProtectedViewMixin,
)
from apps.common.methods.custom_pagination import CustomPagination


class AddressView(ApiKeyProtectedViewMixin, viewsets.GenericViewSet):
    """
    list:
      GET /api/addresses/
      List all addresses.

    create:
      POST /api/addresses/
      Create a new address.

    retrieve:
      GET /api/addresses/{id}/
      Retrieve an address by its id.

    update:
      PUT /api/addresses/{id}/
      Update an address.
    """

    queryset = Address.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "create":
            return AddressCreateSerializer
        return AddressSerializer

    @swagger_auto_schema(
        operation_summary="List Addresses",
        operation_description="Returns a list of all addresses in the system.",
        responses={200: AddressSerializer(many=True)},
    )
    def list(self, request):
        addresses = self.get_queryset()
        page = self.paginate_queryset(addresses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(addresses, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create Address",
        operation_description="Creates a new address and returns the address details.",
        request_body=AddressCreateSerializer,
        responses={201: AddressSerializer, 400: "Bad Request"},
    )
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.save()
        return Response(AddressSerializer(address).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Retrieve Address",
        responses={200: AddressSerializer, 404: "Not Found"},
    )
    def retrieve(self, request, pk=None):
        address = self.get_object()
        serializer = self.get_serializer(address)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update Address",
        operation_description="Update the details of an address.",
        request_body=AddressCreateSerializer,
        responses={200: AddressSerializer, 400: "Bad Request", 404: "Not Found"},
    )
    def update(self, request, pk=None):
        address = self.get_object()
        serializer = self.get_serializer(address, data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.save()
        return Response(AddressSerializer(address).data)

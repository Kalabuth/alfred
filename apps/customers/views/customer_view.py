from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from apps.authentication.mixins.api_key_protected_view_mixin import (
    ApiKeyProtectedViewMixin,
)
from apps.common.methods.custom_pagination import CustomPagination
from apps.customers.models.customer import Customer
from apps.customers.serializers.customers_serializer import (
    CustomerCreateSerializer,
    CustomerSerializer,
)
from apps.addresses.models.address import Address

class CustomerView(ApiKeyProtectedViewMixin, viewsets.GenericViewSet):
    """
    list:
      GET /customers/
      List all customers.

    retrieve:
      GET /customers/{id}/
      Retrieve a customer by its id.

    update:
      PUT /customers/{id}/
      Update a customer.

    partial_update:
      PATCH /customers/{id}/
      Partially update a customer.

    destroy:
      DELETE /customers/{id}/
      Delete a customer.
    """

    queryset = Customer.objects.all()
    parser_classes = [JSONParser]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CustomerCreateSerializer
        return CustomerSerializer

    @swagger_auto_schema(
        operation_summary="List Customers",
        responses={200: CustomerSerializer(many=True), 403: "Forbidden"},
    )
    def list(self, request):
        customers = self.get_queryset()
        page = self.paginate_queryset(customers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Retrieve Customer",
        responses={200: CustomerSerializer, 404: "Not Found", 403: "Forbidden"},
    )
    def retrieve(self, request, pk=None):
        customer = self.get_object()
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update Customer",
        request_body=CustomerCreateSerializer,
        responses={200: CustomerSerializer, 400: "Bad Request", 403: "Forbidden"},
    )
    def update(self, request, pk=None):
        customer = self.get_object()

        address_uuid = request.data.get("address", None)
        if address_uuid:
            try:
                address = Address.objects.get(id=address_uuid)
                customer.current_location = address
            except Address.DoesNotExist:
                return Response(
                    {"detail": "Address not found"}, status=status.HTTP_404_NOT_FOUND
                )

        serializer = self.get_serializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        return Response(CustomerSerializer(customer).data)

    @swagger_auto_schema(
        operation_summary="Partial Update Customer",
        request_body=CustomerCreateSerializer,
        responses={200: CustomerSerializer, 400: "Bad Request", 403: "Forbidden"},
    )
    def partial_update(self, request, pk=None):
        customer = self.get_object()

        address_uuid = request.data.get("address", None)
        if address_uuid:
            try:
                address = Address.objects.get(id=address_uuid)
                customer.address = address
            except Address.DoesNotExist:
                return Response(
                    {"detail": "Address not found"}, status=status.HTTP_404_NOT_FOUND
                )

        serializer = self.get_serializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        return Response(CustomerSerializer(customer).data)

    @swagger_auto_schema(
        operation_summary="Delete Customer",
        responses={204: "No Content", 403: "Forbidden", 404: "Not Found"},
    )
    def destroy(self, request, pk=None):
        customer = self.get_object()
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.urls import include, path
from rest_framework import routers

from apps.addresses.views.address_view import AddressView

router = routers.DefaultRouter()
router.register(r"address", AddressView, basename="address")

urlpatterns = [
    path("", include(router.urls)),
]

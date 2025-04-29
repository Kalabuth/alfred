from django.urls import include, path
from rest_framework import routers

from apps.drivers.views.driver_view import DriverView

router = routers.DefaultRouter()
router.register(r"drivers", DriverView, basename="drivers")

urlpatterns = [
    path("", include(router.urls)),
]

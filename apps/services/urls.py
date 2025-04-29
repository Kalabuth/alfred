from django.urls import include, path
from rest_framework import routers

from apps.services.views.service_view import ServiceView

router = routers.DefaultRouter()
router.register(r"service", ServiceView, basename="service")

urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import include, path
from rest_framework import routers

from apps.customers.views.customer_view import CustomerView

router = routers.DefaultRouter()
router.register(r"customers", CustomerView, basename="customers")

urlpatterns = [
    path("", include(router.urls)),
]

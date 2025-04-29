from django.urls import include, path
from rest_framework import routers

from apps.authentication.views.authentication_view import AuthenticationView

router = routers.DefaultRouter()

router.register(r"auth", AuthenticationView, basename="auth")

urlpatterns = [
    path("", include(router.urls)),
]

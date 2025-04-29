from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.serializers.login_serializer import LoginSerializer
from apps.authentication.serializers.register_serializer import RegisterSerializer
from apps.users.models.user import User


class AuthenticationView(viewsets.GenericViewSet):
    """
    register:
      POST /api/auth/register/
      Register a new user (client or driver).

    login:
      POST /api/auth/login/
      Authenticate a user and retrieve JWT tokens.
    """

    permission_classes = [AllowAny]
    queryset = User.objects.all()
    parser_classes = [JSONParser]

    def get_serializer_class(self):
        if self.action == "register":
            return RegisterSerializer
        if self.action == "login":
            return LoginSerializer
        return None

    @swagger_auto_schema(
        operation_summary="Register new user",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response("User created successfully"),
            400: "Bad Request",
        },
    )
    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = self.get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Login user",
        request_body=LoginSerializer,
        responses={200: openapi.Response("Tokens"), 400: "Invalid credentials"},
    )
    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST
            )

        tokens = self.get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

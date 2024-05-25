from rest_framework.permissions import AllowAny
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers

class SendOTP(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.SendOTPSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class RegisterVerify(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.RegisterVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class LoginVerify(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.LoginVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ForgetPasswordVerify(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.ForgetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class LogoutViewSet(CreateModelMixin, GenericViewSet):
    def create(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(status=HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'error': 'Invalid token'}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'The refresh_token field is required'}, status=HTTP_400_BAD_REQUEST)
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets , status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


from .utils_jwt import get_tokens_for_user
from .models import Profile
from . import serializers
User = get_user_model()
        
class DevLogin(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    
    def create(self, request):
        response = Response()
        user, created = User.objects.get_or_create(phone_number=request.POST.get('phone_number'), email=request.POST.get('email'), is_superuser=True)

        access_token = get_tokens_for_user(user)['access']
        refresh_token = get_tokens_for_user(user)['refresh']
        if created:
            Profile.objects.create(user=user)

        response.set_cookie(key='refreshtoken',
                            value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh': refresh_token,
        }
        return response

class CheckEmail(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.CheckEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        exists = User.objects.filter(email=email).exists()
        return Response({"exists": exists}, status=HTTP_200_OK)

class CheckPhoneNumber(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.CheckPhoneNumberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        exists = User.objects.filter(phone_number=phone_number).exists()
        return Response({"exists": exists}, status=HTTP_200_OK)


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

class ChangePassword(CreateModelMixin, GenericViewSet):
    serializer_class = serializers.ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("The password was changed successfully.", status=HTTP_200_OK)
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
        
class ProfileViewSet(viewsets.GenericViewSet, RetrieveModelMixin, UpdateModelMixin):

    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        profile = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        profile = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
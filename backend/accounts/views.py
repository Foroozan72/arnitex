from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.mixins import CreateModelMixin 
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView, UpdateAPIView

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.utils import translation

from .models import Profile
from . import serializers
from .utils_jwt import get_tokens_for_user
from utils.response import APIResponse
User = get_user_model()

class DevLogin(CreateModelMixin, GenericViewSet):
    """
    API endpoint that allows users to log in using their phone number or email.
    If the user is logging in for the first time, a new profile is created.
    
    Methods:
    - create(request): Handles POST requests to log in a user and returns access and refresh tokens.
    
    Inputs:
    - request: The HTTP request containing 'phone_number' or 'email' in POST data.
    
    Outputs:
    - response: JSON response containing 'access_token' and 'refresh_token' cookies.
    
    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    serializer_class = serializers.ReCaptchaV3Serializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        response = Response()
        if request.POST.get('phone_number'):
            user, created = User.objects.get_or_create(phone_number=request.POST.get('phone_number'))
        elif request.POST.get('email'):
            user, created = User.objects.get_or_create(email=request.POST.get('email'))
        else:
            return Response(_('The phone_number or email field is required.'), status=HTTP_400_BAD_REQUEST)

        if created:
            Profile.objects.create(user=user)

        access_token = get_tokens_for_user(user)['access']
        refresh_token = get_tokens_for_user(user)['refresh']
        
        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh': refresh_token,
        }
        return response

class SendOTP(CreateModelMixin, GenericViewSet):
    """
    API endpoint to send an OTP (One Time Password) for verification purposes.
    
    Methods:
    - create(request, *args, **kwargs): Handles POST requests to send OTP and returns OTP data on success.
    
    Inputs:
    - request: The HTTP request containing required data for sending OTP.
    
    Outputs:
    - response: JSON response containing OTP data on success, or error details on failure.
    
    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    serializer_class = serializers.SendOTPSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse(msg=_('One-time password sent successfully.'), data=serializer.data)

class RegisterVerify(CreateModelMixin, GenericViewSet):
    """
    API endpoint to verify user registration using an OTP.
    
    Methods:
    - create(request, *args, **kwargs): Handles POST requests to verify registration and returns registration data on success.
    
    Inputs:
    - request: The HTTP request containing required data for registration verification.
    
    Outputs:
    - response: JSON response containing registration data on success, or error details on failure.
    
    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    serializer_class = serializers.RegisterVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse(msg=_('Registration was done successfully.'), data=serializer.data, status=HTTP_201_CREATED)

class LoginVerify(CreateModelMixin, GenericViewSet):
    """
    API endpoint to verify user login using an OTP.
    
    Methods:
    - create(request, *args, **kwargs): Handles POST requests to verify login and returns login data on success.
    
    Inputs:
    - request: The HTTP request containing required data for login verification.
    
    Outputs:
    - response: JSON response containing login data on success, or error details on failure.
    
    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    serializer_class = serializers.LoginVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse(msg=_('You are successfully logged in.'), data=serializer.data)

class ForgetPasswordVerify(CreateModelMixin, GenericViewSet):
    """
    API endpoint to verify password reset using an OTP.
    
    Methods:
    - create(request, *args, **kwargs): Handles POST requests to verify password reset and returns verification data on success.
    
    Inputs:
    - request: The HTTP request containing required data for password reset verification.
    
    Outputs:
    - response: JSON response containing verification data on success, or error details on failure.
    
    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    serializer_class = serializers.ForgetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse(msg=_('The password was changed successfully.'), data=serializer.data)

class ChangePassword(CreateModelMixin, GenericViewSet):
    """
    API endpoint to change a user's password.
    
    Methods:
    - create(request, *args, **kwargs): Handles POST requests to change the password and returns a success message on completion.
    
    Inputs:
    - request: The HTTP request containing required data for changing the password.
    
    Outputs:
    - response: JSON response containing a success message on successful password change, or error details on failure.
    
    Permissions:
    - IsAuthenticated: Requires user to be authenticated.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse(msg=_('The password was changed successfully.'), data=serializer.data)

class LogoutViewSet(CreateModelMixin, GenericViewSet):
    """
    API endpoint to log out a user by invalidating their refresh token.
    
    Methods:
    - create(request, *args, **kwargs): Handles POST requests to log out the user and returns a no content response on success.
    
    Inputs:
    - request: The HTTP request containing required data for logging out.
    
    Outputs:
    - response: HTTP 204 No Content response on successful logout, or error details on failure.
    
    Permissions:
    - IsAuthenticated: Requires user to be authenticated.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LogoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse(msg=_('Logout was successful.'), data=serializer.data, status=HTTP_204_NO_CONTENT)

class UserProfileView(ListAPIView, UpdateAPIView):
    """
    API endpoint to retrieve and update user profile information.
    
    Methods:
    - list(request, *args, **kwargs): Handles GET requests to retrieve the authenticated user's profile information.
    - update(request, *args, **kwargs): Handles PUT/PATCH requests to update the authenticated user's profile information.
    
    Inputs:
    - request: The HTTP request for retrieving or updating profile data.
    
    Outputs:
    - response: JSON response containing profile data on successful retrieval or update, or error details on failure.
    
    Permissions:
    - IsAuthenticated: Requires user to be authenticated.
    """
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        instance = self.request.user.profile
        serializer = self.get_serializer(instance)
        return APIResponse(data=serializer.data, status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.request.user.profile
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
            return APIResponse(msg=_('The profile was updated successfully.'), data=serializer.retrieve(instance), status=HTTP_200_OK)

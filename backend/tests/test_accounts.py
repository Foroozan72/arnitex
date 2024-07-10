from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from accounts.utils_otp import get_user_otp  
from accounts.utils_jwt import get_tokens_for_user  

User = get_user_model()

class UserAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.send_otp_url = reverse('accounts:send-otp-list')
        self.register_verify_url = reverse('accounts:register-verify-list')
        self.login_verify_url = reverse('accounts:login-verify-list')
        self.forget_password_verify_url = reverse('accounts:forget-password-verify-list')
        self.change_password_url = reverse('accounts:change-password-list')
        self.logout_url = reverse('accounts:logout-list')

        self.recaptcha_token = 'test_recaptcha_token'
        self.user_data_email = {
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'otp': 123456,
            'recaptcha_token': self.recaptcha_token
        }
        self.user_data_phone = {
            'phone_number': '1234567890',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'otp': 123456,
            'recaptcha_token': self.recaptcha_token
        }

    @patch('accounts.serializers.get_user_otp')
    @patch('accounts.serializers.ReCaptchaV3Serializer.validate_recaptcha_token')
    def test_register_verify_email_success(self, mock_validate_recaptcha_token, mock_get_user_otp):
        mock_get_user_otp.return_value = 123456  # Simulate a valid OTP
        mock_validate_recaptcha_token.return_value = self.recaptcha_token

        response = self.client.post(self.register_verify_url, self.user_data_email, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


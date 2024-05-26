from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from accounts.models import User
from django.core.cache import cache



class TestCheckEmail(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:check-email-list')

    def test_success(self):
        data = {'email': 'example@gmail.com'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_error(self):
        data = {'email': 'example!gmail.com'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestCheckPhoneNumber(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:check-phone_number-list')

    def test_success(self):
        data = {'phone_number': '09123456789'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_error(self):
        data = {'phone_number': '09123456789TX'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestSendOTP(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:send-otp-list')

    def test_success_send_otp_to_phone_number(self):
        data = {'phone_number': '09123456789'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_success_send_otp_to_email(self):
        data = {'email': 'example@gmail.com'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_error(self):
        data = {}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {'email': 'example@gmail.com', 'phone_number': '09123456789'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'email': 'example!gmail.com'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {'phone_number': '09123456789TX'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestRegisterVerify(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:register-verify-list')

    def test_success_register_with_phone_number(self):
        phone_number = '09123456789'
        otp = 123456
        cache.set(phone_number, otp, 180)

        data = {'phone_number': phone_number, 'otp': otp, 'password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_success_register_with_email(self):
        email = 'example@gmail.com'
        otp = 123456
        cache.set(email, otp, 180)

        data = {'email': email, 'otp': otp, 'password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_error(self):
        email = 'example@gmail.com'
        otp = 123456
        cache.set(email, otp, 180)
        data = {'email': email, 'otp': 666666, 'password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        phone_number = '09123456789'
        otp = 123456
        cache.set(email, otp, 180)
        data = {'phone_number': phone_number, 'otp': 666666, 'password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        email = 'example!gmail.com'
        otp = 123456
        cache.set(email, otp, 180)
        data = {'email': email, 'otp': otp, 'password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        phone_number = '09123456789TX'
        otp = 123456
        cache.set(email, otp, 180)
        data = {'phone_number': phone_number, 'otp': otp, 'password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'phone_number': phone_number, 'email': email, 'otp': otp, 'password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestLoginVerify(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:login-verify-list')

    def test_success_login_with_phone_number(self):
        otp = 123456
        phone_number = '09123456789'
        password = 'example_pw'
        cache.set(phone_number, otp, 180)
        User.objects.create_user(phone_number=phone_number, password=password)

        data = {'phone_number': phone_number, 'otp': otp, 'password': password}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_success_login_with_email(self):
        otp = 123456
        email = 'example@gmail.com'
        password = 'example_pw'
        cache.set(email, otp, 180)
        User.objects.create_user(email=email, password=password)

        data = {'email': email, 'otp': otp, 'password': password}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestForgetPassword(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:forget-password-verify-list')

    def test_success_fotget_password_with_phone_number(self):
        otp = 123456
        phone_number = '09123456789'
        cache.set(phone_number, otp, 180)
        User.objects.create_user(phone_number=phone_number)

        data = {'phone_number': phone_number, 'otp': otp, 'new_password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_success_fotget_password_with_email(self):
        otp = 123456
        email = 'example@gmail.com'
        cache.set(email, otp, 180)
        User.objects.create_user(email=email)

        data = {'email': email, 'otp': otp, 'new_password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_error(self):
        otp = 123456
        email = 'example@gmail.com'
        cache.set(email, otp, 180)
        data = {'email': email, 'otp': otp, 'new_password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        otp = 123456
        phone_number = '09123456789TX'
        cache.set(phone_number, otp, 180)
        data = {'phone_number': phone_number, 'otp': otp, 'new_password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        otp = 123456
        email = 'example@gmail.com'
        cache.set(email, otp, 180)
        User.objects.create_user(email=email)
        data = {'email': email, 'otp': 666666, 'new_password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        otp = 123456
        phone_number = '09123456789'
        cache.set(phone_number, otp, 180)
        User.objects.create_user(phone_number=phone_number)
        data = {'phone_number': phone_number, 'otp': 666666, 'new_password': 'example_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestChangePassword(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:change-password-list')
        self.user = User.objects.create_user(phone_number='09123456789', password='example_pw')

    def test_success_fotget_password_with_phone_number(self):
        self.client.force_authenticate(user=self.user)

        data = {'password': 'example_pw', 'new_password': 'example_new_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_error(self):
        self.client.force_authenticate(user=self.user)
        data = {}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'password': 'example_pww', 'new_password': 'example_new_pw'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
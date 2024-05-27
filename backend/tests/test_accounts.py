from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from accounts.models import User
from django.core.cache import cache
from .models import Profile




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

# class ProfileAPITestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='password123')
#         self.client = APIClient()
        
#         # Obtain JWT token for the user
#         refresh = RefreshToken.for_user(self.user)
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

#         def setUp(self):
#         self.client = APIClient()
#         self.register_url = reverse('accounts:login-verify-list')
        
#         # Create profiles
#         # English profile
#         self.profile_en = Profile.objects.create(
#             user=self.user,
#             first_name='John',
#             last_name='Doe',
#             date_of_birth='1990-01-01',
#             address='123 Main St',
#             city='Anytown',
#             state='CA',
#             country='USA',
#             postal_code='12345',
#             national_id='1234567890'
#         )

#         # Persian profile
#         self.profile_fa = Profile.objects.create(
#             user=self.user,
#             first_name='پویا',
#             last_name='کاشانی',
#             date_of_birth='۱۳۶۹-۱۰-۱۰',
#             address='خیابان اصلی ۱۲۳',
#             city='تهران',
#             state=' ',
#             country='ایران',
#             postal_code='۱۲۳۴۵',
#             national_id='۱۲۳۴۵۶۷۸۹۰'
#         )

#         # Arabic profile
#         self.profile_ar = Profile.objects.create(
#             user=self.user,
#             first_name='علی',
#             last_name='دو',
#             date_of_birth='١٩٩٠-٠١-٠١',
#             address='شارع الرئيسي ۱۲۳',
#             city='أي بلد',
#             state='  ',
#             country='الولايات المتحدة العربی',
#             postal_code='۱۲۳٤٥',
#             national_id='۱۲۳٤٥٦٧٨٩٠'
#         )

#     def test_retrieve_profile(self):
#         # English language
#         url_en = reverse('profile-detail', kwargs={'pk': self.profile_en.id})
#         response_en = self.client.get(url_en)
#         self.assertEqual(response_en.status_code, status.HTTP_200_OK)
#         self.assertEqual(response_en.data['first_name'], 'John')

#         # Persian language
#         self.client.cookies['django_language'] = 'fa'
#         url_fa = reverse('profile-detail', kwargs={'pk': self.profile_fa.id})
#         response_fa = self.client.get(url_fa)
#         self.assertEqual(response_fa.status_code, status.HTTP_200_OK)
#         self.assertEqual(response_fa.data['first_name'], 'پویا')

#         # Arabic language
#         self.client.cookies['django_language'] = 'ar'
#         url_ar = reverse('profile-detail', kwargs={'pk': self.profile_ar.id})
#         response_ar = self.client.get(url_ar)
#         self.assertEqual(response_ar.status_code, status.HTTP_200_OK)
#         self.assertEqual(response_ar.data['first_name'], 'علی')
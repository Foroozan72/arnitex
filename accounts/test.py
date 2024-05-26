from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile
from jalali_date import datetime2jalali

class ProfileViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # English profile
        self.profile_en = Profile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            date_of_birth='1990-01-01',
            address='123 Main St',
            city='Anytown',
            state='CA',
            country='USA',
            postal_code='12345',
            national_id='1234567890'
        )

        # Persian profile
        self.profile_fa = Profile.objects.create(
            user=self.user,
            first_name='پویا',
            last_name='کاشانی',
            date_of_birth='۱۳۶۹-۱۰-۱۰',
            address='خیابان اصلی ۱۲۳',
            city='تهران',
            state=' ',
            country='ایران',
            postal_code='۱۲۳۴۵',
            national_id='۱۲۳۴۵۶۷۸۹۰'
        )

        # Arabic profile
        self.profile_ar = Profile.objects.create(
            user=self.user,
            first_name='علی',
            last_name='دو',
            date_of_birth='١٩٩٠-٠١-٠١',
            address='شارع الرئيسي ۱۲۳',
            city='أي بلد',
            state='  ',
            country='الولايات المتحدة العربی',
            postal_code='۱۲۳٤٥',
            national_id='۱۲۳٤٥٦٧٨٩٠'
        )

    def test_retrieve_profile(self):
        # English language
        url_en = reverse('profile-detail', kwargs={'pk': self.profile_en.id})
        response_en = self.client.get(url_en)
        self.assertEqual(response_en.status_code, status.HTTP_200_OK)
        self.assertEqual(response_en.data['first_name'], 'John')

        # Persian language
        self.client.cookies['django_language'] = 'fa'
        url_fa = reverse('profile-detail', kwargs={'pk': self.profile_fa.id})
        response_fa = self.client.get(url_fa)
        self.assertEqual(response_fa.status_code, status.HTTP_200_OK)
        self.assertEqual(response_fa.data['first_name'], 'پویا')

        # Arabic language
        self.client.cookies['django_language'] = 'ar'
        url_ar = reverse('profile-detail', kwargs={'pk': self.profile_ar.id})
        response_ar = self.client.get(url_ar)
        self.assertEqual(response_ar.status_code, status.HTTP_200_OK)
        self.assertEqual(response_ar.data['first_name'], 'علی')

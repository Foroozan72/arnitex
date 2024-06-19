from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from .models import Country, City

class TestCitySerializer(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.country = Country.objects.create(title="Test Country", flag="test_flag.png", is_show=True)
        self.city_create_url = reverse('country-read') 

    def test_create_city_success(self):
        data = {
            'title': 'New City',
            'is_show': True,
            'country': self.country.id
        }
        response = self.client.post(self.city_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New City')
        self.assertEqual(response.data['is_show'], True)
        self.assertEqual(response.data['country'], self.country.id)

    def test_create_city_error_missing_title(self):
        data = {
            'is_show': True,
            'country': self.country.id
        }
        response = self.client.post(self.city_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_city_error_missing_country(self):
        data = {
            'title': 'New City',
            'is_show': True,
        }
        response = self.client.post(self.city_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_city_error_invalid_country(self):
        data = {
            'title': 'New City',
            'is_show': True,
            'country': 9999  
        }
        response = self.client.post(self.city_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


#for city

class TestCitySerializer(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.country = Country.objects.create(title="Test Country", flag="test_flag.png", is_show=True)
        self.city_create_url = reverse('city-read')  # Update with the actual URL name

    def test_create_city_success(self):
        data = {
            'title': 'New City',
            'is_show': True,
            'country': self.country.id
        }
        response = self.client.post(self.city_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New City')
        self.assertEqual(response.data['is_show'], True)
        self.assertEqual(response.data['country'], self.country.id)

    def test_create_city_error_missing_title(self):
        data = {
            'is_show': True,
            'country': self.country.id
        }
        response = self.client.post(self.city_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_city_error_missing_country(self):
        data = {
            'title': 'New City',
            'is_show': True,
        }
        response = self.client.post(self.city_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_city_error_invalid_country(self):
        data = {
            'title': 'New City',
            'is_show': True,
            'country': 9999 
        }
        response = self.client.post(self.city_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

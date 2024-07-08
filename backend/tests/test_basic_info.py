from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from basic_info.models import Country
from django.contrib.auth import get_user_model

User = get_user_model()

class TestCountryViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=self.superuser)
        self.country_url = reverse('basic_info:country-list')
        self.country_detail_url = lambda pk: reverse('basic_info:country-detail', kwargs={'pk': pk})

    def test_create_country(self):
        data = {'title': 'Test Country', 'flag': 'test_flag.png', 'is_show': True}
        response = self.client.post(self.country_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Country')

    def test_list_countries(self):
        Country.objects.create(title='Country 1', flag='flag1.png', is_show=True)
        Country.objects.create(title='Country 2', flag='flag2.png', is_show=True)
        response = self.client.get(self.country_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_country(self):
        country = Country.objects.create(title='Country 1', flag='flag1.png', is_show=True)
        response = self.client.get(self.country_detail_url(country.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Country 1')

    def test_update_country(self):
        country = Country.objects.create(title='Country 1', flag='flag1.png', is_show=True)
        data = {'title': 'Updated Country', 'flag': 'updated_flag.png', 'is_show': False}
        response = self.client.put(self.country_detail_url(country.pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Country')

    def test_partial_update_country(self):
        country = Country.objects.create(title='Country 1', flag='flag1.png', is_show=True)
        data = {'title': 'Partially Updated Country'}
        response = self.client.patch(self.country_detail_url(country.pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Partially Updated Country')

    def test_delete_country(self):
        country = Country.objects.create(title='Country 1', flag='flag1.png', is_show=True)
        response = self.client.delete(self.country_detail_url(country.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Country.objects.count(), 0)

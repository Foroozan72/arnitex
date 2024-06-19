from rest_framework.test import APITestCase
from .models import Country, City
from .serializers import CountrySerializer, CitySerializer

class SerializerTests(APITestCase):

    def setUp(self):
        self.country = Country.objects.create(title="Test Country", flag="test_flag.png", is_show=True)
        self.city = City.objects.create(title="Test City", is_show=True, country=self.country)

        self.country_serializer = CountrySerializer(instance=self.country)
        self.city_serializer = CitySerializer(instance=self.city)

    def test_city_serializer(self):
        data = self.city_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title', 'is_show', 'country']))
        self.assertEqual(data['title'], 'Test City')
        self.assertEqual(data['is_show'], True)
        self.assertEqual(data['country'], self.country.id)

    def test_country_serializer(self):
        data = self.country_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title', 'flag', 'is_show', 'cities']))
        self.assertEqual(data['title'], 'Test Country')
        self.assertEqual(data['flag'], 'test_flag.png')
        self.assertEqual(data['is_show'], True)
        self.assertEqual(len(data['cities']), 1)
        self.assertEqual(data['cities'][0]['title'], 'Test City')

    def test_city_serializer_create(self):
        country = Country.objects.create(title="New Country", flag="new_flag.png", is_show=True)
        data = {'title': 'New City', 'is_show': True, 'country': country.id}
        serializer = CitySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        city = serializer.save()
        self.assertEqual(city.title, 'New City')
        self.assertEqual(city.is_show, True)
        self.assertEqual(city.country, country)

    def test_country_serializer_create(self):
        data = {'title': 'New Country', 'flag': 'new_flag.png', 'is_show': True}
        serializer = CountrySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        country = serializer.save()
        self.assertEqual(country.title, 'New Country')
        self.assertEqual(country.flag, 'new_flag.png')
        self.assertEqual(country.is_show, True)

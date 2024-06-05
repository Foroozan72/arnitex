import requests
from django.core.management.base import BaseCommand
from basic_info.models import Country, City
from django.conf import settings


class Command(BaseCommand):
    help = 'Fetch data from web service and populate models'

    def handle(self, *args, **kwargs):
        url = settings.WEB_SERVICE_URL
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-200 status codes
            data = response.json()
            self.populate_data(data)
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except requests.RequestException as e:
            self.stderr.write(f'Failed to fetch data: {e}')

    def populate_data(self, data):
        for country_data in data.get('data', []):
            country_name = country_data.get('country')
            if country_name:
                country, created = Country.objects.get_or_create(title=country_name)
                cities = country_data.get('cities', [])
                for city_name in cities:
                    if city_name:
                        City.objects.get_or_create(title=city_name, country=country)
                    else:
                        self.stderr.write(f'Skipped empty city name for country: {country_name}')
            else:
                self.stderr.write('Skipped empty country name')

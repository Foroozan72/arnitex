import requests
from django.core.management.base import BaseCommand
from basic_info.models import Country, State, City

class Command(BaseCommand):
    help = 'Fetches and imports country, state, and city data from an external API'

    def handle(self, *args, **kwargs):
        url = 'https://restcountries.com/v3.1/all'
        response = requests.get(url)
        if response.status_code == 200:
            countries = response.json()
            for country_data in countries:
                country_title = country_data.get('name', {}).get('common', '')
                if country_title:
                    country, created = Country.objects.update_or_create(
                        title=country_title,
                        defaults={'is_show': True}
                    )
                    # Assuming states data is available in the country data
                    states_data = country_data.get('states', [])
                    for state_data in states_data:
                        state_title = state_data.get('name', '')
                        if state_title:
                            state, created = State.objects.update_or_create(
                                title=state_title,
                                country=country,
                                defaults={'is_show': True}
                            )
                            # Assuming cities data is available in the state data
                            cities_data = state_data.get('cities', [])
                            for city_data in cities_data:
                                city_title = city_data.get('name', '')
                                if city_title:
                                    City.objects.update_or_create(
                                        title=city_title,
                                        state=state,
                                        defaults={'is_show': True}
                                    )
            self.stdout.write(self.style.SUCCESS('Successfully imported country, state, and city data'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data'))

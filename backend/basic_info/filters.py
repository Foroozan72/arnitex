import django_filters
from .models import Country , City

class CountryFilter(django_filters.FilterSet):
    class Meta:
        model = Country
        fields = {
            'title': ['icontains'],
            'is_show': ['exact'],
        }

class CityFilter(django_filters.FilterSet):
    class Meta:
        model = City
        fields = {
            'title': ['icontains'],
            'is_show': ['exact'],
            'country': ['exact'],
        }
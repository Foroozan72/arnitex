import pycountry
from basic_info.models import City, Country

flag_base_url = "https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/"
for country in pycountry.countries:
    flag_url = f"{flag_base_url}{country.alpha_2.lower()}.svg"
    obj, created = Country.objects.get_or_create(title=country.name, flag=flag_url)

for subdivision in pycountry.subdivisions:
    country = Country.objects.get(title=subdivision.country.name)
    obj, created = City.objects.get_or_create(title=subdivision.name, country=country)

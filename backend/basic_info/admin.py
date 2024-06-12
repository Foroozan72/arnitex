from django.contrib import admin
from .models import Country , City, CryptoCurrency

class CountryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
admin.site.register(Country, CountryAdmin)

class CityAdmin(admin.ModelAdmin):
    list_display = ['title', 'country']
    list_filter = ['country']
    search_fields = ['title']
admin.site.register(City, CityAdmin)

class CryptoCurrencyAdmin(admin.ModelAdmin):
    list_display = ['coin_name', 'coin_id', 'is_active']
    search_fields = ['coin_name', 'coin_id']
    list_filter = ['is_active']
admin.site.register(CryptoCurrency, CryptoCurrencyAdmin)




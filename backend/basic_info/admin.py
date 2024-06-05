from django.contrib import admin
from .models import Country , City 


class CityAdmin(admin.ModelAdmin):
    list_display = ['title', 'country']
    list_filter = ['country']
    search_fields = ['title']

class CountryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)




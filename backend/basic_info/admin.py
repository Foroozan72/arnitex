from django.contrib import admin
from .models import Country , City 

class CountryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
admin.site.register(Country, CountryAdmin)

class CityAdmin(admin.ModelAdmin):
    list_display = ['title', 'country']
    list_filter = ['country']
    search_fields = ['title']
admin.site.register(City, CityAdmin)




from django.contrib import admin
from .models import Country , City , State


class CityAdmin(admin.ModelAdmin):
    list_display = ['title', 'country']
    list_filter = ['country']
    search_fields = ['title']

class StateAdmin(admin.ModelAdmin):
    list_display = ['title', 'city']
    list_filter = ['city__country']

class CountryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

admin.site.register(State, StateAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)




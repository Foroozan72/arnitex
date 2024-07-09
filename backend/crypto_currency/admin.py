from django.contrib import admin
from .models import CryptoCurrency
# Register your models here.


class CryptoCurrencyAdmin(admin.ModelAdmin):
    list_display = ['coin_name', 'coin_id', 'is_active']
    search_fields = ['coin_name', 'coin_id']
    list_filter = ['is_active']
    ordering = ('created_at', )
admin.site.register(CryptoCurrency, CryptoCurrencyAdmin)

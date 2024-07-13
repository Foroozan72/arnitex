from django.contrib import admin
from .models import Asset, BankAccount
# Register your models here.

admin.site.register(Asset)
admin.site.register(BankAccount)
# admin.site.register(Transaction)
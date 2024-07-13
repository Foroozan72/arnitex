from django.contrib import admin
from .models import Asset, BankAccount
from .models import Coin, Network, Transaction
# Register your models here.

admin.site.register(Asset)
admin.site.register(BankAccount)
admin.site.register(Coin)
admin.site.register(Network)
admin.site.register(Transaction)
# admin.site.register(Transaction)
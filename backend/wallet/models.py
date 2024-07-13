import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from crypto_currency.models import CryptoCurrency
from utils.enums import TransactionActionChoices
from utils.models import TimeStamp, UUID
User = get_user_model()

class Asset(TimeStamp, UUID):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_asset', verbose_name=_('User'))
    coin = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE, verbose_name=_('Coin'))
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=0.0, verbose_name=_('Amount'))

    class Meta:
        verbose_name, verbose_name_plural = _('Asset'), _('Assets')

    def __str__(self):
        return f'{self.user.profile.first_name} {self.user.profile.last_name} - {self.coin} - {self.amount}'

class BankAccount(TimeStamp, UUID):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='bank_accounts_user', verbose_name=_('User'))
    BIN = models.CharField(max_length=50, verbose_name=_(' Bank Identification Number'))
    IBAN = models.CharField(max_length=50, verbose_name=_('International Bank Account Number'))
    bank_name = models.CharField(max_length=50, verbose_name=_('Bank name'))
    image = models.ImageField(default='bank/images/', verbose_name=_('Image'))

    class Meta:
        verbose_name, verbose_name_plural = _('Bank Account'), _('Bank Accounts')

    def __str__(self):
        return f'{self.user.profile.first_name} {self.user.profile.last_name} - {self.bank_name}'
        
from django.db import models
from utils.models import TimeStamp, UUID
from django.utils.translation import gettext_lazy as _


class Country(TimeStamp, UUID):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    flag = models.CharField(max_length=200, verbose_name=_('Flag'))
    is_show = models.BooleanField(default=True, verbose_name=_('Is_show'))


    def __str__(self):
        return f"{self.title} - {self.is_show}"

class City(TimeStamp, UUID):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    is_show = models.BooleanField(default=True, verbose_name=_('Is_show'))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities', verbose_name=_('Country'))

    def __str__(self):
        return f"{self.title} - {self.is_show}"

class CryptoCurrency(TimeStamp, UUID):
    coin_id = models.CharField(max_length=100, verbose_name=_('Coin id'))
    coin_name = models.CharField(max_length=100, verbose_name=_('Coin name'))
    coin_symbol = models.CharField(max_length=100, default='backend/basic_info/images/metamask.png' , verbose_name=_('Coin symbol'))
    coin_image = models.CharField(max_length=500,default='backend/basic_info/images/metamask.png' , verbose_name=_('Coin image'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active?'))

    class Meta:
        verbose_name, verbose_name_plural = _('Crypto currency'), _('Crypto currencie')

class Wallet(models.Model):
    wallet_id = models.CharField(max_length=100 , verbose_name=_('Wallet'))
    wallet_name = models.CharField(max_length=100, verbose_name=_('Wallet name'))
    description = models.TextField(blank=True, null=True , verbose_name=_('Description'))
    website_url = models.URLField(verbose_name=_('Website url'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active?'))
    logo = models.ImageField(upload_to='wallet/logos/', blank=True, null=True , verbose_name=_('Logo'))
    qr_code = models.ImageField(upload_to='wallet/ qrcodes/', blank=True, null=True , verbose_name=_('QR code'))

    def __str__(self):
        return self.name
    

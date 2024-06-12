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
    is_active = models.BooleanField(default=True, verbose_name=_('Is active?'))

    class Meta:
        verbose_name, verbose_name_plural = _('Crypto currency'), _('Crypto currencie')

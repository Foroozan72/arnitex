from django.db import models
from utils.models import TimeStamp, UUID
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CryptoCurrency(TimeStamp, UUID):
    coin_id = models.CharField(max_length=100, verbose_name=_('Coin id'))
    coin_name = models.CharField(max_length=100, verbose_name=_('Coin name'))
    coin_symbol = models.CharField(max_length=100, default='backend/basic_info/images/metamask.png' , verbose_name=_('Coin symbol'))
    coin_image = models.CharField(max_length=500,default='backend/basic_info/images/metamask.png' , verbose_name=_('Coin image'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active?'))

    class Meta:
        verbose_name, verbose_name_plural = _('Crypto currency'), _('Crypto currencie')

    def __str__(self):
        return self.coin_name
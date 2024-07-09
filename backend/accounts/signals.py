from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile
from wallet.models import Asset
from crypto_currency.models import CryptoCurrency
User = get_user_model()

@receiver(post_save, sender=User)
def create_Inf_basic_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        toman_obj, created = CryptoCurrency.objects.get_or_create(coin_id='0', coin_name='Toman')
        Asset.objects.create(user=instance, coin=toman_obj)

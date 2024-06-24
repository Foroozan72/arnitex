from django.db import models
from utils.models import TimeStamp, UUID
from django.utils.translation import gettext_lazy as _
from utils.enums import TransactionActionChoices

class Wallet(TimeStamp, UUID):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, verbose_name=_('User'))
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0.0, verbose_name=_('Balance'))

    class Meta:
        verbose_name, verbose_name_plural = _('Wallet'), _('Wallets')

    def __str__(self):
        return f'{self.user.phone_number} Wallet'

class Transaction(UUID):
    user_wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, verbose_name=_('User wallet'))
    action = models.CharField(choices=TransactionActionChoices.choices, max_length=20, verbose_name=_('Action'))
    amount = models.DecimalField(max_digits=20, decimal_places=8, verbose_name=_('Amount'))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Timestamp'))

    # internal transfer
    sender = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='sent_transactions', verbose_name=_('Sender'))
    receiver = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='received_transactions', verbose_name=_('Receiver'))

    class Meta:
        verbose_name, verbose_name_plural = _('Transaction'), _('Transactions')

    def __str__(self):
        return f'{self.user_wallet.user.username} {self.action} of {self.amount}'

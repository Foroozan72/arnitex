from django.db import models
from django.utils.translation import gettext as _

# Ticket
class TicketStatusChoices(models.TextChoices):
    ANSWERED = 'answered', _('Answered')
    CLOSE = 'close', _('Close')
    AWAITING = 'awaiting', _('Awaiting')
    WITHDRAW = 'withdraw', _('Withdraw')

class TicketContentPositionChoices(models.TextChoices):
    USER = 'user', _('User')
    ADMIN = 'admin', _('Admin')

# Wallet
class TransactionActionChoices(models.TextChoices):
    DEPOSIT = 'deposit', _('Deposit')
    WITHDRAW = 'withdraw', _('Withdraw')
    INTERNAL_TRANSFER = 'internal_transfer', _('Internal transfer')
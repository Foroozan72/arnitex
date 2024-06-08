from django.db import models
from django.utils.translation import gettext as _


class TicketStatusChoices(models.TextChoices):
    ANSWERED = 'answered', _('Answered')
    CLOSE = 'close', _('Close')
    AWAITING = 'awaiting', _('Awaiting')
    WITHDRAW = 'withdraw', _('Withdraw')

class TicketContentPositionChoices(models.TextChoices):
    USER = 'user', _('User')
    ADMIN = 'admin', _('Admin')
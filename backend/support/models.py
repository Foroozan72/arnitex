from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from utils.models import TimeStamp, UUID
from utils.enums import TicketStatusChoices, TicketContentPositionChoices
User = get_user_model()

class TicketUnit(TimeStamp, UUID):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    is_show = models.BooleanField(default=True, verbose_name=_('Is show?'))
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name, verbose_name_plural = _('Ticket Unit'), _('Ticket Units')

class Ticket(TimeStamp, UUID):
    tracking_code = models.CharField(max_length=13, null=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    unit = models.ForeignKey(TicketUnit, on_delete=models.SET_NULL, null=True, verbose_name=_('Unit'))
    status = models.CharField(max_length=10, choices=TicketStatusChoices.choices, default=TicketStatusChoices.AWAITING, verbose_name=_('Status'))

    class Meta:
        verbose_name, verbose_name_plural = _('Ticket'), _('Tickets')

class TicketContent(TimeStamp, UUID):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name=_('Ticket'))
    admin = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('admin'))
    content = models.TextField(null=True, blank=True, verbose_name=_('Content'))
    # images = models.ManyToManyField(Images, verbose_name=_('Images'))
    position = models.CharField(max_length=10, choices=TicketContentPositionChoices.choices, default=TicketContentPositionChoices.USER, verbose_name=_('Position'))
    
    class Meta:
        verbose_name, verbose_name_plural = _('Ticket content'), _('Ticket contents')

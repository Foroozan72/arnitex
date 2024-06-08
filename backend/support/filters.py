import django_filters
from .models import TicketUnit, Ticket, TicketContent

class TicketUnitFilter(django_filters.FilterSet):
    class Meta:
        model = TicketUnit
        fields = ['is_show']
        
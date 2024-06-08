
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import TicketUnit, Ticket, TicketContent
from . import serializers
from .permissions import IsSuperuser
from .filters import TicketUnitFilter
# ---- Ticket----
# USER Section
class TicketUnitViewSet(viewsets.ModelViewSet):
    queryset = TicketUnit.objects.all()
    serializer_class = serializers.TicketUnitSerializer
    permission_classes = [IsSuperuser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = TicketUnitFilter
    ordering_fields = ['-created_at']
    search_fields = ['title']

    def get_permissions(self):
        if self.action in ['create', 'delete', 'update']:
            self.permission_classes = [IsSuperuser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(TicketUnitViewSet, self).get_permissions()

class CreateTicketViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CreateTicketSerializer

class TicketViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user).order_by('-created_at')
    
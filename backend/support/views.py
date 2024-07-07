
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext as _

from .models import TicketUnit, Ticket, TicketContent
from . import serializers
from .permissions import IsSuperuser
from .filters import TicketUnitFilter
from utils.response import APIResponseMixin
# ---- Ticket----
# USER Section
class TicketUnitViewSet(APIResponseMixin, viewsets.ModelViewSet):
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.api_response(msg=_('The ticket unit was created successfully.'), data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.api_response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.api_response(msg=_('The ticket unit was updated successfully.'), data=serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.api_response(msg=_('The ticket unit was deleted.'))

class CreateTicketViewSet(APIResponseMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CreateTicketSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.api_response(msg=_('The ticket was created successfully.'), data=serializer.data)

class TicketViewSet(APIResponseMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user).order_by('-created_at')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.api_response(msg=_('.'), data=serializer.data)
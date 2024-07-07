from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import TicketUnit, Ticket, TicketContent
from utils.classes import GenerateTrackingCode
from utils.enums import TicketStatusChoices
from utils.response import CustomValidationError

class TicketUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketUnit
        fields = ['id', 'title', 'is_show', 'updated_at', 'created_at']
        extra_kwargs = {
            'is_show': {'default': True},
        }

class CreateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['unit', 'updated_at', 'created_at']
        extra_kwargs = {
            'unit': {'required': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

class TicketSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()
    class Meta:
        depth = 1
        model = Ticket
        fields = ['id', 'tracking_code', 'unit', 'status', 'updated_at', 'created_at']
        read_only_fields = ['id', 'tracking_code', 'unit', 'updated_at', 'created_at']

    def get_updated_at(self, obj):
        content_obj = TicketContent.objects.filter(ticket=obj).last()
        return content_obj.updated_at if content_obj else obj.updated_at

    def validate(self, attrs):
        if attrs["status"] != TicketStatusChoices.WITHDRAW:
            raise CustomValidationError(_(
                f"The status value entered is not correct. The value of the status can only be {TicketStatusChoices.WITHDRAW}"))
        return attrs
    
    def save(self, **kwargs):
        return self.validated_data

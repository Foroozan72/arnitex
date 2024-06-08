from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket
from utils.classes import GenerateTrackingCode

@receiver(post_save, sender=Ticket)
def create_ticket_tracking_code(sender, instance, created, **kwargs):
    if created:
        instance.tracking_code = GenerateTrackingCode.generate_tracking_code(sender)
        instance.save()

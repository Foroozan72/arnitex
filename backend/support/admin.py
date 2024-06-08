from django.contrib import admin
from .models import TicketUnit, Ticket, TicketContent
# Register your models here.

class TicketUnitAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_show']
    list_filter = ['is_show']
    search_fields = ['title']
admin.site.register(TicketUnit, TicketUnitAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display = ['tracking_code', 'user', 'unit', 'status']
    list_filter = ['status']
    search_fields = ['tracking_code']
    readonly_fields = ("tracking_code",)
    ordering = ['-created_at']
admin.site.register(Ticket, TicketAdmin)

class TicketContentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'admin', 'position']
    list_filter = ['position']
    search_fields = ['ticket__tracking_code', 'content']
    ordering = ['-created_at']
admin.site.register(TicketContent, TicketContentAdmin)
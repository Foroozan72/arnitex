from django.contrib import admin
from .models import Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'created_at', 'created_at')
    search_fields = ('image', )
    ordering = ('-created_at',)
    
admin.site.register(Image, ImageAdmin)
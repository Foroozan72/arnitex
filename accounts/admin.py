
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class UserAdmin(UserAdmin):
    list_display = (
        'email', 'phone_number', 'is_staff',
        )
    list_filter = (
        'is_verified', 'is_staff', 'is_superuser',
        )

    ordering = ('-date_joined', )

    fieldsets = (
        (None, {
            'fields': ('email', 'phone_number', 'password')
        }),
        ('Permissions', {
            'fields': (
                'is_verified', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login',)
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'phone_number', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': (
                'is_verified', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
    )
admin.site.register(User, UserAdmin)
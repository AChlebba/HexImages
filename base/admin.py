from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Tier

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'tier'
        )
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'tier')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tier)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Tier, Image, Link, CustomSize, CustomThumbnail

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
admin.site.register(Image)
admin.site.register(Link)
admin.site.register(CustomSize)
admin.site.register(CustomThumbnail)


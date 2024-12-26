from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Import your User model

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'role', 'voterID', 'wallet_address', 'is_active']  # Add 'wallet_address' here
    search_fields = ['username', 'voterID', 'wallet_address']  # Make 'wallet_address' searchable
    ordering = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Keep your original fields
        ('Personal info', {'fields': ('role', 'voterID', 'wallet_address')}),  # Add 'wallet_address' to personal info
        ('Permissions', {'fields': ('is_active', 'is_staff')}),  # Keep your permissions
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'voterID', 'wallet_address', 'is_active', 'is_staff'),  # Include 'wallet_address' here
        }),
    )

# Register the custom admin class
admin.site.register(User, CustomUserAdmin)

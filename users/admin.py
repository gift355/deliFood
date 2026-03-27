from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CustomerProfile

# This allows you to edit the Profile (Address) directly on the User page
class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'Customer Profile'

class CustomUserAdmin(UserAdmin):
    # Add your custom fields to the User list view in Admin
    list_display = ('username', 'email', 'phone_number', 'role', 'is_staff')
    
    # Add your custom fields to the Edit User page
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone_number', 'role')}),
    )
    
    # Add your custom fields to the "Add User" page
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('phone_number', 'role')}),
    )
    
    inlines = [CustomerProfileInline]

# Register your models
admin.site.register(User, CustomUserAdmin)

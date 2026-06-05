from django.contrib import admin
from .models import DriverProfile

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    # This makes it easy to see driver details in a clean table view
    list_display = ('id', 'user', 'total_earnings', 'is_online')
    list_filter = ('is_online',)
    search_fields = ('user__username', 'user__email')
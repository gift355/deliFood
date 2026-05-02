# Register your models here.
from django.contrib import admin
from .models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    # What you see in the list view
    list_display = ('name', 'address', 'is_active')
    # Search by name or address
    search_fields = ('name', 'address')
    # Automatically creates the slug (e.g. "Mega Chicken" -> "mega-chicken")
    prepopulated_fields = {'slug': ('name',)}
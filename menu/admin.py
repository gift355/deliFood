from django.contrib import admin
from .models import FoodItem

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    # Displays the price, category, and which restaurant owns it
    list_display = ('name', 'restaurant', 'price', 'category', 'available')
    # Filter sidebar for quick navigation
    list_filter = ('category', 'available', 'restaurant')
    search_fields = ('name', 'description')

from django.contrib import admin

# Register your models here.


# Register your models here.
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 1. See everything important at a glance
    list_display = ('order_number', 'status', 'driver', 'payout_amount', 'created_at')
    
    # 2. Add a sidebar to filter by status (Essential for testing!)
    list_filter = ('status', 'created_at')
    
    # 3. Allow you to change the status directly from the list page
    # This saves you thousands of clicks during development
    list_editable = ('status',)
    
    # 4. Search by order number or customer name
    search_fields = ('order_number', 'customer__username')
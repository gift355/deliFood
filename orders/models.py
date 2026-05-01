# Create your models here.
from django.db import models
from django.conf import settings
from drivers.models import DriverProfile # Import your driver profile

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('picked_up', 'Picked Up'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Links
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')

    # Data
    order_number = models.CharField(max_length=10, unique=True)
    delivery_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2) # Price customer pays
    
    # This is what goes to the driver
    payout_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_number} - {self.status}"